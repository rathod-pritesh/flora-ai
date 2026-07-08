<script>
	import { Card, CardContent } from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Textarea } from "$lib/components/ui/textarea/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Sparkles, MessageSquare, Plus, Trash, Send, Copy, Check } from "lucide-svelte";

	let conversations = $state([
		{ id: 1, title: "NextJS to Svelte migration strategy", snippet: "Reviewing code structures..." },
		{ id: 2, title: "LinkedIn career optimization plan", snippet: "To create premium reach..." }
	]);

	let activeId = $state(null);
	let searchQuery = $state("");
	let inputPrompt = $state("");
	let isGenerating = $state(false);
	let chatHistory = $state([]);
	let copyStatus = $state(false);

	const filteredConversations = $derived(
		conversations.filter(c => c.title.toLowerCase().includes(searchQuery.toLowerCase()))
	);

	function startNewConversation() {
		const newId = Date.now();
		conversations = [
			{ id: newId, title: "New AI Workspace Draft", snippet: "Drafting empty session..." },
			...conversations
		];
		activeId = newId;
		chatHistory = [];
		inputPrompt = "";
	}

	function deleteConversation(id, e) {
		e.stopPropagation();
		conversations = conversations.filter(c => c.id !== id);
		if (activeId === id) {
			activeId = null;
			chatHistory = [];
		}
	}

	function selectConversation(id) {
		activeId = id;
		if (id === 1) {
			chatHistory = [
				{ role: "user", text: "What is the best way to migrate a Next.js App router codebase to SvelteKit?" },
				{ role: "assistant", text: "To migrate from Next.js App Router to SvelteKit:\n\n1. **Routing:** Map `app/path/page.tsx` directly to `src/routes/path/+page.svelte`.\n2. **Layouts:** Map `layout.tsx` to `+layout.svelte` using standard child nodes.\n3. **Data Fetching:** Convert server components fetch functions to SvelteKit server-side `load` hooks." }
			];
		} else if (id === 2) {
			chatHistory = [
				{ role: "user", text: "Optimize my LinkedIn career summary for AI Product roles." },
				{ role: "assistant", text: "High-impact summary:\n\n\"AI Product Architect | Transforming complex ML research into premium user experiences. Expert in Svelte, NextJS, Python, and scalable cloud designs. Helping teams deploy agentic workflows that double efficiency.\"" }
			];
		} else {
			chatHistory = [];
		}
	}

	function handleSend() {
		if (!inputPrompt.trim()) return;
		chatHistory = [...chatHistory, { role: "user", text: inputPrompt }];
		const promptToSend = inputPrompt;
		inputPrompt = "";
		isGenerating = true;

		setTimeout(() => {
			chatHistory = [...chatHistory, { 
				role: "assistant", 
				text: `Processed prompt: "${promptToSend}"\n\nHere is your career copilot draft response. Custom layouts can be structured with tailwind CSS grids. Svelte 5 updates are instantaneous.` 
			}];
			isGenerating = false;
			conversations = conversations.map(c => 
				c.id === activeId ? { ...c, title: promptToSend.slice(0, 32) + "...", snippet: promptToSend } : c
			);
		}, 800);
	}

	function handleCopy(text) {
		navigator.clipboard.writeText(text);
		copyStatus = true;
		setTimeout(() => copyStatus = false, 1500);
	}
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-6 h-[calc(100vh-8.5rem)] overflow-hidden">
	<!-- Sidebar conversation List -->
	<div class="md:col-span-1 border border-stone-200 bg-white rounded-xl flex flex-col overflow-hidden h-full">
		<div class="p-3 border-b border-stone-150 flex flex-col gap-2">
			<Button onclick={startNewConversation} class="w-full bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 font-sans">
				<Plus class="size-4 mr-2" />
				New Draft
			</Button>
			<Input
				bind:value={searchQuery}
				placeholder="Search drafts..."
				class="h-8 text-xs border-stone-200 font-sans"
			/>
		</div>
		<div class="flex-1 overflow-y-auto p-2 space-y-1">
			{#each filteredConversations as item}
				<div
					class="w-full flex items-center justify-between text-left rounded-lg border transition-all text-xs font-sans {activeId === item.id ? 'bg-stone-50 border-stone-300' : 'border-transparent hover:bg-stone-50/50'}"
				>
					<button
						onclick={() => selectConversation(item.id)}
						class="flex-1 flex items-start gap-2 p-2.5 min-w-0 outline-none select-none text-left {activeId === item.id ? 'font-semibold' : ''}"
					>
						<MessageSquare class="size-4 text-stone-400 mt-0.5 shrink-0" />
						<div class="min-w-0">
							<p class="text-stone-850 truncate">{item.title}</p>
							<p class="text-stone-400 truncate mt-0.5">{item.snippet}</p>
						</div>
					</button>
					<button
						onclick={(e) => deleteConversation(item.id, e)}
						class="text-stone-400 hover:text-red-500 p-2 mr-1 shrink-0 outline-none"
						title="Delete Session"
					>
						<Trash class="size-3.5" />
					</button>
				</div>
			{/each}
		</div>
	</div>

	<!-- Main Chat workspace -->
	<div class="md:col-span-3 border border-stone-200 bg-white rounded-xl flex flex-col overflow-hidden h-full">
		{#if activeId === null}
			<!-- Empty State -->
			<div class="flex-1 flex flex-col items-center justify-center p-8 text-center bg-stone-50/20">
				<div class="p-3.5 rounded-full bg-[#A16207]/10 text-[#A16207] mb-4">
					<Sparkles class="size-8" />
				</div>
				<h3 class="text-lg font-bold text-stone-900 font-sans">AI Copilot Workspace</h3>
				<p class="text-stone-400 font-sans text-xs mt-2 max-w-sm">
					Start a new draft session or select an existing conversation snippet from the panel to run code analysis, summary drafting, or resume updates.
				</p>
				<Button onclick={startNewConversation} class="mt-4 bg-[#A16207] hover:bg-[#A16207]/90 h-9 text-xs font-sans text-white">
					Create Custom Session
				</Button>
			</div>
		{:else}
			<!-- Chat Content Area -->
			<div class="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
				{#each chatHistory as chat}
					<div class="flex gap-4 {chat.role === 'user' ? 'justify-end' : 'justify-start'}">
						<div class="max-w-[85%] rounded-lg p-3.5 text-xs font-sans leading-relaxed {chat.role === 'user' ? 'bg-[#A16207]/10 text-stone-800' : 'bg-stone-50 border border-stone-200 text-stone-900'}">
							<div class="flex justify-between items-start gap-4 mb-2">
								<span class="font-bold text-[10px] uppercase tracking-wider {chat.role === 'user' ? 'text-[#A16207]' : 'text-stone-500'}">
									{chat.role === 'user' ? 'You' : 'Copilot'}
								</span>
								{#if chat.role === 'assistant'}
									<button onclick={() => handleCopy(chat.text)} class="text-stone-400 hover:text-stone-600 outline-none select-none">
										{#if copyStatus}
											<Check class="size-3.5 text-emerald-600" />
										{:else}
											<Copy class="size-3.5" />
										{/if}
									</button>
								{/if}
							</div>
							<p class="whitespace-pre-wrap">{chat.text}</p>
						</div>
					</div>
				{/each}
				{#if isGenerating}
					<div class="flex gap-4 justify-start">
						<div class="max-w-[80%] rounded-lg p-3.5 bg-stone-50 border border-stone-200 text-stone-400 text-xs font-sans flex items-center gap-2">
							<div class="animate-bounce shrink-0 size-2 bg-stone-400 rounded-full"></div>
							<div class="animate-bounce delay-75 shrink-0 size-2 bg-stone-400 rounded-full"></div>
							<div class="animate-bounce delay-150 shrink-0 size-2 bg-stone-400 rounded-full"></div>
							<span>Copilot thinking...</span>
						</div>
					</div>
				{/if}
			</div>

			<!-- Input area -->
			<div class="p-3 border-t border-stone-150 bg-stone-50/50 flex gap-2 items-end">
				<Textarea
					bind:value={inputPrompt}
					onkeydown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
					placeholder="Type your message here... (Enter to send, Shift+Enter for newline)"
					class="flex-1 bg-white border-stone-200 min-h-[44px] max-h-[120px] text-xs font-sans"
				/>
				<Button onclick={handleSend} disabled={!inputPrompt.trim() || isGenerating} class="bg-[#A16207] text-white hover:bg-[#A16207]/90 size-11 p-0 shrink-0 font-sans">
					<Send class="size-4" />
				</Button>
			</div>
		{/if}
	</div>
</div>
