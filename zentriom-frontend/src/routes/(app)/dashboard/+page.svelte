<script>
	import { appState } from "$lib/states/app.svelte.js";
	import { env } from "$env/dynamic/public";
	import { goto } from "$app/navigation";
	import {
		Sparkles,
		Languages,
		Share2,
		Briefcase,
		FileText,
		Wrench,
		Plus,
		Send,
		Copy,
		Check,
		ThumbsUp,
		ThumbsDown
	} from "lucide-svelte";
	import { getAuthHeaders } from "$lib/services/auth";

	// API Endpoint from environment variable
	const apiBase = env.PUBLIC_API_URL || "http://127.0.0.1:8000";

	// Suggested action cards list
	const suggestedCards = [
		{
			title: "LinkedIn Post",
			desc: "Generate professional posts or milestone updates for your network.",
			icon: Share2,
			path: "/linkedin"
		},
		{
			title: "Grammar Fix",
			desc: "Refine readability, correctness, and structure of your documents.",
			icon: Languages,
			path: "/grammar"
		},
		{
			title: "Explain Code",
			desc: "Get an interactive step-by-step breakdown of complex logic.",
			icon: Sparkles,
			path: "/code-explainer"
		},
		{
			title: "Bug Fix",
			desc: "AI-powered debugging assistance currently under development. Future support will include runtime analysis, stack trace interpretation, and intelligent fix suggestions.",
			icon: Wrench,
			underDevelopment: true
		},
		{
			title: "Resume Review",
			desc: "Resume analysis and personalized improvement recommendations are currently under development.",
			icon: FileText,
			underDevelopment: true
		},
		{
			title: "Job Match",
			desc: "Skill-based opportunity discovery and intelligent job matching are currently under development.",
			icon: Briefcase,
			underDevelopment: true
		}
	];

	// Component States
	let messages = $state([]);
	let inputValue = $state("");
	let isTyping = $state(false);
	let copiedMessageId = $state(null);

	// Get user initials for avatar
	const getInitials = (userName) => {
		if (!userName) return "PR";
		const parts = userName.trim().split(/\s+/);
		if (parts.length === 0) return "PR";
		if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
		return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
	};

	// Helper to scroll parent main to bottom
	function scrollToBottom() {
		const mainEl = document.querySelector('main');
		if (mainEl) {
			mainEl.scrollTo({ top: mainEl.scrollHeight, behavior: 'smooth' });
		}
	}

	// Helper to get formatted local time
	function getCurrentTime() {
		const now = new Date();
		let hours = now.getHours();
		const minutes = now.getMinutes().toString().padStart(2, '0');
		const ampm = hours >= 12 ? 'PM' : 'AM';
		hours = hours % 12;
		hours = hours ? hours : 12;
		return `${hours}:${minutes} ${ampm}`;
	}

	// Format text lines: bold, italic, bullets
	function formatLine(line) {
		let escaped = line
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;");

		escaped = escaped.replace(/\*\*(.*?)\*\*/g, "<strong class='font-bold text-stone-900'>$1</strong>");
		escaped = escaped.replace(/\*(.*?)\*/g, "<em class='italic'>$1</em>");

		if (escaped.trim().startsWith("- ") || escaped.trim().startsWith("* ")) {
			const bulletText = escaped.replace(/^(\s*[-*]\s+)/, "");
			return `<span class="inline-block pl-2 relative before:content-['•'] before:absolute before:left-0 before:text-[#A16207]">${bulletText}</span>`;
		}

		return escaped;
	}

	// Parse text sections to separate code blocks from prose
	function parseMarkdown(text) {
		if (!text) return [];
		const parts = text.split("```");
		return parts.map((part, index) => {
			const isCode = index % 2 === 1;
			if (isCode) {
				const lines = part.split("\n");
				const lang = lines[0].trim();
				const code = lines.slice(1).join("\n").trim();
				return { type: 'code', code, lang };
			} else {
				return { type: 'text', content: part };
			}
		});
	}

	// Send message to the backend FastAPI /chat endpoint
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
			const response = await fetch(`${apiBase}/chat`, {
				method: "POST",
				headers: getAuthHeaders(),
				body: JSON.stringify({
					prompt: text
				})
			});

			if (!response.ok) {
				throw new Error(
					data.detail || 'Something went wrong. Please try again'
				);
			}

			const data = await response.json();
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
				text: "⚠️ **Error:** Unable to connect to the Zentriom AI backend. Please ensure the server is running at http://127.0.0.1:8000 and try again.",
				timestamp: getCurrentTime(),
				liked: false,
				disliked: false,
				isError: true
			};
			messages = [...messages, errorMsg];
		} finally {
			isTyping = false;
			setTimeout(() => {
				scrollToBottom();
			}, 50);
		}
	}

	// Handle sending messages
	function handleSend() {
		if (!inputValue.trim()) return;
		const text = inputValue.trim();
		inputValue = "";
		sendMessageToBackend(text);
	}

	// Keydown event handler (Enter to send)
	function handleKeyDown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSend();
		}
	}

	// Copy message content
	function handleCopyMessage(id, text) {
		navigator.clipboard.writeText(text);
		copiedMessageId = id;
		setTimeout(() => {
			if (copiedMessageId === id) {
				copiedMessageId = null;
			}
		}, 2000);
	}

	// Like toggle
	function handleLike(id) {
		messages = messages.map(msg => {
			if (msg.id === id) {
				return { ...msg, liked: !msg.liked, disliked: false };
			}
			return msg;
		});
	}

	// Dislike toggle
	function handleDislike(id) {
		messages = messages.map(msg => {
			if (msg.id === id) {
				return { ...msg, disliked: !msg.disliked, liked: false };
			}
			return msg;
		});
	}

	// New Chat reset with smooth scroll to top of main container
	function handleNewChat() {
		messages = [];
		inputValue = "";
		
		const mainEl = document.querySelector('main');
		if (mainEl) {
			mainEl.scrollTo({ top: 0, behavior: 'smooth' });
		}
	}

	// custom greeting
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
			greeting: 'Good Night',
			subtitle: [
				'Working late tonight?',
				'Need a quick helping hand?',
				'Let’s solve a few more problems.',
				'How can Zentriom assist you tonight?'
			]
		};
	}

	let welcome = $state(getGreeting());
	const randomSubtitle = welcome.subtitle[
		Math.floor(Math.random() * welcome.subtitle.length)
	];
</script>

<div class="flex flex-col min-h-[calc(100vh-8rem)] relative">
	<!-- Chat Header -->
	<div class="flex items-center justify-between border-b border-stone-200 bg-white p-4 shadow-xs rounded-xl mb-6">
		<div class="flex items-center gap-2">
			<div class="p-1.5 rounded-lg bg-[#A16207]/10 text-[#A16207]">
				<Sparkles class="size-5 shrink-0" />
			</div>
			<span class="text-base font-bold text-stone-900 font-sans">Zentriom AI</span>
		</div>

		<div class="flex items-center gap-3 relative">
			<!-- New Chat Button -->
			<button
				onclick={handleNewChat}
				class="flex items-center gap-1 rounded-lg border border-stone-200 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 hover:bg-stone-50 select-none outline-none cursor-pointer"
			>
				<Plus class="size-3.5" />
				<span>New Chat</span>
			</button>
		</div>
	</div>

	<!-- Scrollable Content -->
	{#if messages.length === 0}
		<!-- Welcome State -->
		<div class="flex-1 flex flex-col items-center justify-center py-12 max-w-4xl mx-auto w-full">
			<div class="text-center space-y-3 mb-10">
				<h2 class="text-3xl font-bold tracking-tight text-stone-900 font-sans md:text-4xl">
					{welcome.greeting}, {appState.user?.name ? appState.user.name.split(' ')[0] : 'Pritesh'} 👋
				</h2>
				<p class="text-stone-500 font-sans text-sm md:text-base max-w-xl mx-auto leading-relaxed">
					{randomSubtitle}
				</p>
			</div>

			<!-- Suggested Prompts Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full px-4">
				{#each suggestedCards as card}
					{#if card.underDevelopment}
						<div
							class="relative flex flex-col text-left p-5 rounded-xl border border-stone-200 bg-stone-50 opacity-70 select-none outline-none"
						>
							<div class="absolute top-4 right-4 bg-stone-200 text-stone-600 border border-stone-300 text-[8px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full font-sans">
								UNDER DEVELOPMENT
							</div>
							<div class="p-2.5 rounded-lg bg-stone-100 text-stone-400 w-fit mb-4">
								<card.icon class="size-5 shrink-0" />
							</div>
							<h3 class="text-sm font-semibold text-stone-400 font-sans mb-1">
								{card.title}
							</h3>
							<p class="text-xs text-stone-400 font-sans leading-relaxed flex-1">
								{card.desc}
							</p>
						</div>
					{:else}
						<button
							onclick={() => goto(card.path)}
							class="flex flex-col text-left p-5 rounded-xl border border-stone-200 bg-white hover:border-[#A16207]/40 hover:shadow-sm hover:shadow-[#A16207]/5 transition-all group outline-none cursor-pointer"
						>
							<div class="p-2.5 rounded-lg bg-stone-100 text-stone-600 group-hover:bg-[#A16207]/10 group-hover:text-[#A16207] transition-colors w-fit mb-4">
								<card.icon class="size-5 shrink-0" />
							</div>
							<h3 class="text-sm font-semibold text-stone-800 font-sans mb-1 group-hover:text-[#A16207] transition-colors">
								{card.title}
							</h3>
							<p class="text-xs text-stone-400 font-sans leading-relaxed flex-1">
								{card.desc}
							</p>
						</button>
					{/if}
				{/each}
			</div>
		</div>
	{:else}
		<!-- Chat Area -->
		<div class="flex-1 space-y-6 pb-24 max-w-4xl mx-auto w-full px-4">
			{#each messages as msg}
				<div class="flex gap-4 {msg.sender === 'user' ? 'justify-end' : 'justify-start'}">
					<!-- AI Avatar (shows on left) -->
					{#if msg.sender === 'ai'}
						<div class="size-9 rounded-full bg-[#A16207]/10 flex items-center justify-center border border-[#A16207]/20 shrink-0 text-[#A16207]">
							<Sparkles class="size-4" />
						</div>
					{/if}

					<!-- Message Bubble -->
					<div class="flex flex-col max-w-[85%] sm:max-w-[75%] gap-1">
						<div class="rounded-2xl px-4 py-3 text-sm font-sans leading-relaxed border shadow-xs
							{msg.sender === 'user' 
								? 'bg-stone-900 text-stone-50 border-stone-800 rounded-tr-none' 
								: msg.isError
									? 'bg-red-50 text-red-800 border-red-200 rounded-tl-none font-medium'
									: 'bg-white text-stone-800 border-stone-200 rounded-tl-none'}"
						>
							{#if msg.sender === 'ai'}
								{#each parseMarkdown(msg.text) as block}
									{#if block.type === 'code'}
										<div class="my-3 rounded-lg overflow-hidden border border-stone-200 font-mono text-xs shadow-inner">
											{#if block.lang}
												<div class="bg-stone-100 border-b border-stone-200 px-3 py-1.5 text-[10px] text-stone-500 font-sans font-semibold flex items-center justify-between">
													<span>{block.lang.toUpperCase()}</span>
													<button 
														onclick={() => handleCopyMessage(msg.id + block.code.length, block.code)}
														class="hover:text-stone-800 transition-colors flex items-center gap-1 font-normal outline-none cursor-pointer"
													>
														Copy Code
													</button>
												</div>
											{/if}
											<pre class="bg-stone-50 p-3 overflow-x-auto text-stone-800 leading-relaxed"><code>{block.code}</code></pre>
										</div>
									{:else}
										<div class="space-y-2">
											{#each block.content.split("\n") as paragraph}
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

						<!-- Metadata & Actions -->
						<div class="flex items-center gap-3 px-1 mt-1 text-[10px] text-stone-400 font-sans">
							<span>{msg.timestamp}</span>

							{#if msg.sender === 'ai' && !msg.isError}
								<span class="text-stone-300">|</span>
								
								<!-- Copy Button -->
								<button 
									onclick={() => handleCopyMessage(msg.id, msg.text)}
									class="hover:text-stone-700 transition-colors flex items-center gap-0.5 outline-none cursor-pointer"
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

								<span class="text-stone-300">|</span>

								<!-- Like/Dislike -->
								<button 
									onclick={() => handleLike(msg.id)}
									class="hover:text-stone-700 transition-colors flex items-center gap-0.5 outline-none cursor-pointer {msg.liked ? 'text-[#A16207]' : ''}"
									title="Like"
								>
									<ThumbsUp class="size-3" />
								</button>
								<button 
									onclick={() => handleDislike(msg.id)}
									class="hover:text-stone-700 transition-colors flex items-center gap-0.5 outline-none cursor-pointer {msg.disliked ? 'text-red-600' : ''}"
									title="Dislike"
								>
									<ThumbsDown class="size-3" />
								</button>
							{/if}
						</div>
					</div>

					<!-- User Avatar (shows on right) -->
					{#if msg.sender === 'user'}
						<div class="size-9 rounded-full bg-stone-200 flex items-center justify-center border border-stone-300 shrink-0 text-stone-700 text-xs font-bold font-sans">
							{getInitials(appState.user?.name)}
						</div>
					{/if}
				</div>
			{/each}

			<!-- Thinking/Typing State -->
			{#if isTyping}
				<div class="flex gap-4 justify-start">
					<div class="size-9 rounded-full bg-[#A16207]/10 flex items-center justify-center border border-[#A16207]/20 shrink-0 text-[#A16207] animate-pulse">
						<Sparkles class="size-4" />
					</div>
					<div class="flex flex-col gap-1">
						<div class="bg-white border border-stone-200 rounded-2xl rounded-tl-none px-4 py-3.5 shadow-xs">
							<div class="flex items-center gap-1.5 py-1">
								<span class="size-1.5 rounded-full bg-stone-400 animate-bounce" style="animation-delay: 0ms"></span>
								<span class="size-1.5 rounded-full bg-stone-400 animate-bounce" style="animation-delay: 150ms"></span>
								<span class="size-1.5 rounded-full bg-stone-400 animate-bounce" style="animation-delay: 300ms"></span>
							</div>
						</div>
						<span class="text-[10px] text-stone-400 font-sans px-1">Zentriom AI is thinking...</span>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Sticky Bottom Input -->
	<div class="sticky bottom-0 bg-[#FAFAF9] -mx-4 px-4 md:-mx-6 md:px-6 lg:-mx-8 lg:px-8 pt-4 pb-6 z-30">
		<div class="max-w-4xl mx-auto w-full">
			<div class="relative flex flex-col w-full rounded-2xl border border-stone-200 bg-white shadow-sm focus-within:border-[#A16207] focus-within:ring-2 focus-within:ring-[#A16207]/10 transition-all p-3 gap-2">
				<!-- Textarea -->
				<textarea
					bind:value={inputValue}
					onkeydown={handleKeyDown}
					placeholder="Ask Zentriom anything..."
					class="w-full bg-transparent border-0 outline-none resize-none font-sans text-sm text-stone-850 placeholder:text-stone-400 min-h-[48px] max-h-[180px] focus:ring-0 p-1 leading-relaxed field-sizing-content"
					rows="1"
				></textarea>

				<!-- Action Buttons Row -->
				<div class="flex items-center justify-end border-t border-stone-100 pt-2 text-stone-450">
					<div class="flex items-center gap-3">
						<!-- Shortcut Hint -->
						<span class="hidden sm:inline text-[10px] text-stone-400 font-sans select-none">
							Press <kbd class="px-1 py-0.5 rounded bg-stone-100 border border-stone-200 text-stone-500 font-mono text-[9px] shadow-2xs">Enter</kbd> to send
						</span>

						<!-- Send Button -->
						<button
							onclick={handleSend}
							disabled={!inputValue.trim() || isTyping}
							class="flex size-8 items-center justify-center rounded-lg transition-all select-none outline-none cursor-pointer
								{inputValue.trim() && !isTyping
									? 'bg-[#A16207] text-white hover:bg-[#A16207]/90' 
									: 'bg-stone-100 text-stone-300 pointer-events-none'}"
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
