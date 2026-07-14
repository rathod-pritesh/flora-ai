<script>
	import { onMount } from 'svelte';
	import { appState } from '$lib/states/app.svelte.js';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { env } from '$env/dynamic/public';
	import { goto } from '$app/navigation';
	import {
		Sparkles,
		Languages,
		Share2,
		Briefcase,
		FileText,
		Wrench,
		Send,
		Copy,
		Check
	} from 'lucide-svelte';
	import { getAuthHeaders, sendChatMessage } from '$lib/services/auth';
	import { toast } from 'svelte-sonner';

	const suggestedCards = [
		{
			title: 'LinkedIn Post',
			desc: 'Generate professional LinkedIn posts tailored to your experience and career goals.',
			icon: Share2,
			path: '/linkedin'
		},
		{
			title: 'Grammar Fix',
			desc: 'Improve grammar, readability, and writing quality with AI-powered assistance.',
			icon: Languages,
			path: '/grammar'
		},
		{
			title: 'Explain Code',
			desc: 'Understand complex programming logic with interactive, step-by-step explanations.',
			icon: Sparkles,
			path: '/code-explainer'
		},
		{
			title: 'Bug Fix',
			desc: 'Resolve software bugs and debug runtime errors using intelligent code suggestions.',
			icon: Wrench,
			underDevelopment: true
		},
		{
			title: 'Resume Review',
			desc: 'Analyze resume quality and get personalized feedback to improve your profile.',
			icon: FileText,
			underDevelopment: true
		},
		{
			title: 'Job Match',
			desc: 'Discover relevant career opportunities based on your skills and experience.',
			icon: Briefcase,
			underDevelopment: true
		}
	];

	let messages = $state([]);
	let inputValue = $state('');
	let isTyping = $state(false);
	let copiedMessageId = $state(null);
	let imageFailed = $state(false);

	const getInitials = (userName) => {
		if (!userName) return 'TU';
		const parts = userName.trim().split(/\s+/);
		if (parts.length === 0) return 'TU';
		if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
		return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
	};

	function scrollToBottom() {
		const mainEl = document.querySelector('main');
		if (mainEl) {
			mainEl.scrollTo({ top: mainEl.scrollHeight, behavior: 'smooth' });
		}
	}

	function getCurrentTime() {
		const now = new Date();
		let hours = now.getHours();
		const minutes = now.getMinutes().toString().padStart(2, '0');
		const ampm = hours >= 12 ? 'PM' : 'AM';
		hours = hours % 12;
		hours = hours ? hours : 12;
		return `${hours}:${minutes} ${ampm}`;
	}

	function formatLine(line) {
		let escaped = line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

		escaped = escaped.replace(
			/\*\*(.*?)\*\*/g,
			"<strong class='font-bold text-stone-900'>$1</strong>"
		);
		escaped = escaped.replace(/\*(.*?)\*/g, "<em class='italic'>$1</em>");

		if (escaped.trim().startsWith('- ') || escaped.trim().startsWith('* ')) {
			const bulletText = escaped.replace(/^(\s*[-*]\s+)/, '');
			return `<span class="inline-block pl-2 relative before:content-['•'] before:absolute before:left-0 before:text-[#A16207]">${bulletText}</span>`;
		}

		return escaped;
	}

	function parseMarkdown(text) {
		if (!text) return [];
		const parts = text.split('```');
		return parts.map((part, index) => {
			const isCode = index % 2 === 1;
			if (isCode) {
				const lines = part.split('\n');
				const lang = lines[0].trim();
				const code = lines.slice(1).join('\n').trim();
				return { type: 'code', code, lang };
			} else {
				return { type: 'text', content: part };
			}
		});
	}

	async function sendMessageToBackend(text) {
		if (!text.trim() || isTyping) return;

		const userMsg = {
			id: Date.now(),
			sender: 'user',
			text: text,
			timestamp: getCurrentTime()
		};
		messages = [...messages, userMsg];
		isTyping = true;

		setTimeout(() => {
			scrollToBottom();
		}, 50);

		try {
			const data = await sendChatMessage(text);
			const responseText = data.response;

			const aiMsg = {
				id: Date.now() + 1,
				sender: 'ai',
				text: responseText,
				timestamp: getCurrentTime(),
				liked: false,
				disliked: false
			};
			messages = [...messages, aiMsg];
		} catch (error) {
			console.error(error);
			const errorMsg = {
				id: Date.now() + 1,
				sender: 'ai',
				text: '⚠️ **Error:** Unable to connect to the Zentriom AI backend.',
				timestamp: getCurrentTime(),
				liked: false,
				disliked: false,
				isError: true
			};
			messages = [...messages, errorMsg];
			toast.error('Unable to contact Zentriom AI. Please try again.');
		} finally {
			isTyping = false;
			setTimeout(() => {
				scrollToBottom();
			}, 50);
		}
	}

	function handleSend() {
		if (!inputValue.trim()) return;
		const text = inputValue.trim();
		inputValue = '';
		sendMessageToBackend(text);
	}

	function handleKeyDown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSend();
		}
	}

	function handleCopyMessage(id, text) {
		navigator.clipboard.writeText(text);
		copiedMessageId = id;
		setTimeout(() => {
			if (copiedMessageId === id) {
				copiedMessageId = null;
			}
		}, 2000);
	}

	function handleNewChat() {
		messages = [];
		inputValue = '';
		const mainEl = document.querySelector('main');
		if (mainEl) {
			mainEl.scrollTo({ top: 0, behavior: 'smooth' });
		}
	}

	function getGreeting() {
		const hour = new Date().getHours();
		if (hour >= 5 && hour < 12) {
			return {
				greeting: 'Good Morning',
				subtitle: [
					'What would you like to do today?',
					'Ready to boost your productivity?',
					'Let’s accomplish something great today.',
					'How can Zentriom help you this morning?'
				]
			};
		}
		if (hour >= 12 && hour < 17) {
			return {
				greeting: 'Good Afternoon',
				subtitle: [
					'How is your day going?',
					'Need help finishing today’s tasks?',
					'Let’s keep the momentum going.',
					'What can I help you with this afternoon?'
				]
			};
		}
		if (hour >= 17 && hour < 21) {
			return {
				greeting: 'Good Evening',
				subtitle: [
					'Wrapping up your day?',
					'Need help before you sign off?',
					'Let’s finish today strong.',
					'What would you like to work on this evening?'
				]
			};
		}
		return {
			greeting: 'Welcome back',
			subtitle: [
				"What would you like to create, improve, or learn tonight?",
				"Need a hand wrapping up today's tasks?",
				"Let's make a little more progress before the day ends."
			]
		};
	}

	let welcome = $state(getGreeting());
	const randomSubtitle = welcome.subtitle[Math.floor(Math.random() * welcome.subtitle.length)];

	onMount(() => {
		appState.onNewChat = handleNewChat;
		return () => {
			appState.onNewChat = null;
		};
	});
</script>

<div class="flex flex-col min-h-[calc(100vh-8rem)] relative">
	{#if messages.length === 0}
		<div class="flex-1 flex flex-col items-center justify-center py-12 max-w-4xl mx-auto w-full">
			<div class="text-center space-y-3 mb-10">
				<h2 class="text-3xl font-bold tracking-tight text-foreground font-sans md:text-4xl">
					{welcome.greeting}, {authStore.user?.name ? authStore.user.name.split(' ')[0] : 'User'} 👋
				</h2>
				<p
					class="text-muted-foreground font-sans text-sm md:text-base max-w-xl mx-auto leading-relaxed"
				>
					{randomSubtitle}
				</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full px-4">
				{#each suggestedCards as card}
					{#if card.underDevelopment}
						<div
							class="relative flex flex-col text-left p-5 rounded-xl border border-border bg-muted opacity-70 select-none outline-none"
						>
							<div
								class="absolute top-4 right-4 bg-muted text-muted-foreground border border-border text-[8px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full font-sans"
							>
								UNDER DEVELOPMENT
							</div>
							<div class="p-2.5 rounded-lg bg-background text-muted-foreground w-fit mb-4">
								<card.icon class="size-5 shrink-0" />
							</div>
							<h3 class="text-sm font-semibold text-muted-foreground/80 font-sans mb-1">
								{card.title}
							</h3>
							<p class="text-xs text-muted-foreground font-sans leading-relaxed flex-1">
								{card.desc}
							</p>
						</div>
					{:else}
						<button
							onclick={() => goto(card.path)}
							class="flex flex-col text-left p-5 rounded-xl border border-border bg-card hover:border-[#A16207]/40 hover:shadow-sm hover:shadow-[#A16207]/5 transition-all group outline-none cursor-pointer"
						>
							<div
								class="p-2.5 rounded-lg bg-muted text-foreground group-hover:bg-[#A16207]/10 group-hover:text-[#A16207] transition-colors w-fit mb-4"
							>
								<card.icon class="size-5 shrink-0" />
							</div>
							<h3
								class="text-sm font-semibold text-foreground font-sans mb-1 group-hover:text-[#A16207] transition-colors"
							>
								{card.title}
							</h3>
							<p class="text-xs text-muted-foreground font-sans leading-relaxed flex-1">
								{card.desc}
							</p>
						</button>
					{/if}
				{/each}
			</div>
		</div>
	{:else}
		<div class="flex-1 space-y-6 pb-24 max-w-4xl mx-auto w-full px-4 text-foreground">
			{#each messages as msg}
				<div class="flex gap-4 {msg.sender === 'user' ? 'justify-end' : 'justify-start'}">
					{#if msg.sender === 'ai'}
						<div
							class="size-9 rounded-full bg-card flex items-center justify-center border border-border shrink-0 select-none"
						>
							<img src="/logo.png" class="size-5 object-contain" alt="Zentriom Logo" />
						</div>
					{/if}

					<div class="flex flex-col max-w-[85%] sm:max-w-[75%] gap-1">
						<div
							class="rounded-2xl px-4 py-3 text-sm font-sans leading-relaxed border shadow-xs
							{msg.sender === 'user'
								? 'bg-stone-900 dark:bg-stone-800 text-stone-50 border-stone-800 dark:border-stone-700 rounded-tr-none'
								: msg.isError
									? 'bg-red-50 text-red-800 border-red-200 rounded-tl-none font-medium'
									: 'bg-card text-foreground border-border rounded-tl-none'}"
						>
							{#if msg.sender === 'ai'}
								{#each parseMarkdown(msg.text) as block}
									{#if block.type === 'code'}
										<div
											class="my-3 rounded-lg overflow-hidden border border-border font-mono text-xs shadow-inner"
										>
											{#if block.lang}
												<div
													class="bg-muted border-b border-border px-3 py-1.5 text-[10px] text-muted-foreground font-sans font-semibold flex items-center justify-between"
												>
													<span>{block.lang.toUpperCase()}</span>
													<button
														onclick={() =>
															handleCopyMessage(msg.id + block.code.length, block.code)}
														class="hover:text-[#A16207] transition-colors flex items-center gap-1 font-normal outline-none cursor-pointer"
													>
														Copy Code
													</button>
												</div>
											{/if}
											<pre
												class="bg-muted/50 p-3 overflow-auto max-h-[350px] text-foreground leading-relaxed"><code
													>{block.code}</code
												></pre>
										</div>
									{:else}
										<div class="space-y-2">
											{#each block.content.split('\n') as paragraph}
												{#if paragraph.trim()}
													<p class="leading-relaxed">
														{@html formatLine(paragraph)}
													</p>
												{/if}
											{/each}
										</div>
									{/if}
								{/each}
							{:else}
								<div class="whitespace-pre-wrap">{msg.text}</div>
							{/if}
						</div>

						<div
							class="flex items-center gap-3 px-1 mt-1 text-[10px] text-muted-foreground font-sans"
						>
							<span>{msg.timestamp}</span>

							{#if msg.sender === 'ai' && !msg.isError}
								<span class="text-stone-300">|</span>

								<button
									onclick={() => handleCopyMessage(msg.id, msg.text)}
									class="hover:text-[#A16207] transition-colors flex items-center gap-0.5 outline-none cursor-pointer"
									title="Copy message"
								>
									{#if copiedMessageId === msg.id}
										<Check class="size-3 text-emerald-600" />
										<span class="text-emerald-600 font-semibold">Copied!</span>
									{:else}
										<Copy class="size-3" />
										<span>Copy</span>
									{/if}
								</button>
							{/if}
						</div>
					</div>

					{#if msg.sender === 'user'}
						<div
							class="size-9 rounded-full bg-muted flex items-center justify-center border border-border shrink-0 text-foreground text-xs font-bold font-sans overflow-hidden"
						>
							{#if authStore.user?.picture && !imageFailed}
								<img
									src={authStore.cachedAvatar || authStore.user.picture}
									class="size-full object-cover"
									alt="User Avatar"
									onerror={() => (imageFailed = true)}
								/>
							{:else}
								{getInitials(authStore.user?.name)}
							{/if}
						</div>
					{/if}
				</div>
			{/each}

			{#if isTyping}
				<div class="flex gap-4 justify-start">
					<div
						class="size-9 rounded-full bg-card flex items-center justify-center border border-border shrink-0 animate-pulse select-none"
					>
						<img src="/logo.png" class="size-5 object-contain" alt="Zentriom Logo" />
					</div>
					<div class="flex flex-col gap-1">
						<div
							class="bg-card border border-border rounded-2xl rounded-tl-none px-4 py-3.5 shadow-xs"
						>
							<div class="flex items-center gap-1.5 py-1">
								<span
									class="size-1.5 rounded-full bg-stone-400 animate-bounce"
									style="animation-delay: 0ms"
								></span>
								<span
									class="size-1.5 rounded-full bg-stone-400 animate-bounce"
									style="animation-delay: 150ms"
								></span>
								<span
									class="size-1.5 rounded-full bg-stone-400 animate-bounce"
									style="animation-delay: 300ms"
								></span>
							</div>
						</div>
						<span class="text-[10px] text-muted-foreground font-sans px-1"
							>Zentriom AI is thinking...</span
						>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<div
		class="sticky bottom-[-1rem] md:bottom-[-1.5rem] lg:bottom-[-2rem] bg-gradient-to-t from-background via-background to-transparent -mx-4 md:-mx-6 lg:-mx-8 px-4 md:px-6 lg:px-8 pt-6 pb-4 md:pb-6 z-30"
	>
		<div class="max-w-4xl mx-auto w-full">
			<div
				class="relative flex flex-col w-full rounded-2xl border border-border bg-card shadow-md focus-within:border-[#A16207] focus-within:ring-2 focus-within:ring-[#A16207]/10 transition-all p-3 gap-2"
			>
				<textarea
					bind:value={inputValue}
					onkeydown={handleKeyDown}
					placeholder="Ask Zentriom anything..."
					class="w-full bg-transparent border-0 outline-none resize-none font-sans text-sm text-foreground placeholder:text-muted-foreground min-h-[48px] max-h-[180px] focus:ring-0 p-1 leading-relaxed field-sizing-content"
					rows="1"></textarea>

				<div
					class="flex items-center justify-end border-t border-border pt-2 text-muted-foreground"
				>
					<div class="flex items-center gap-3">
						<span class="hidden sm:inline text-[10px] text-muted-foreground font-sans select-none">
							Press <kbd
								class="px-1 py-0.5 rounded bg-muted border border-border text-muted-foreground font-mono text-[9px] shadow-2xs"
								>Enter</kbd
							> to send
						</span>

						<button
							onclick={handleSend}
							disabled={!inputValue.trim() || isTyping}
							class="flex size-8 items-center justify-center rounded-lg transition-all select-none outline-none cursor-pointer
								{inputValue.trim() && !isTyping
								? 'bg-[#A16207] text-white hover:bg-[#A16207]/90'
								: 'bg-muted text-muted-foreground/50 pointer-events-none'}"
							title="Send message"
						>
							<Send class="size-4" />
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
