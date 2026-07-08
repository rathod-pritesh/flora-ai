<script>
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Textarea } from "$lib/components/ui/textarea/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Badge } from "$lib/components/ui/badge/index.js";
	import { Share2, Copy, Check, Sparkles } from "lucide-svelte";

	let topic = $state("The power of Svelte 5 runes in modern enterprise design systems");
	let audience = $state("Software Engineers and Product Leaders");
	let selectedTone = $state("Professional");
	let isGenerating = $state(false);
	let generatedPost = $state("");
	let hashtags = $state([]);
	let copyStatus = $state(false);

	const tones = ["Professional", "Creative", "Confident", "Insightful"];

	function generatePost() {
		if (!topic.trim()) return;
		isGenerating = true;

		setTimeout(() => {
			if (selectedTone === "Professional") {
				generatedPost = `🚀 Thrilled to share my latest architecture strategy on designing scalable agentic AI frontends.\n\nBy leveraging Svelte 5 runes and Tailwind CSS v4, we build lightweight layout systems that keep complexity low and compile with extreme reliability.\n\nHow is your team handling state updates in Svelte? Let's discuss in the comments!`;
				hashtags = ["AIProduct", "SvelteKit", "Productivity", "WebDev"];
			} else {
				generatedPost = `💡 Let's talk about building premium web applications. Topic: "${topic}"\n\nDesign is not just what it looks like, it's how it works. By keeping frontend code understandable and eliminating overengineered abstractions, we create long-term stability.\n\nThoughts? 👇`;
				hashtags = ["DesignSystem", "Engineering", "Innovation", "CareerGrowth"];
			}
			isGenerating = false;
		}, 800);
	}

	function handleCopy() {
		const fullText = `${generatedPost}\n\n${hashtags.map(t => `#${t}`).join(" ")}`;
		navigator.clipboard.writeText(fullText);
		copyStatus = true;
		setTimeout(() => copyStatus = false, 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
	<!-- Left Side: Prompt Builder -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardHeader class="border-b border-stone-100">
			<CardTitle class="text-base font-bold text-stone-900 font-sans">Post Parameters</CardTitle>
			<CardDescription class="text-xs text-stone-400 font-sans">Set topics and context for your post</CardDescription>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<!-- Topic -->
			<div class="space-y-1">
				<label for="topic" class="text-xs font-semibold text-stone-700 font-sans">Topic / Details</label>
				<Textarea
					id="topic"
					bind:value={topic}
					placeholder="What is your post about?"
					class="min-h-[80px] bg-white border-stone-200 text-xs font-sans"
				/>
			</div>

			<!-- Audience -->
			<div class="space-y-1">
				<label for="audience" class="text-xs font-semibold text-stone-700 font-sans">Target Audience</label>
				<Input
					id="audience"
					bind:value={audience}
					placeholder="e.g. recruiters, developers..."
					class="h-9 bg-white border-stone-200 text-xs font-sans"
				/>
			</div>

			<!-- Tones -->
			<div class="space-y-1.5">
				<span class="text-xs font-semibold text-stone-700 font-sans block">Tone</span>
				<div class="flex flex-wrap gap-2">
					{#each tones as tone}
						<button
							onclick={() => selectedTone = tone}
							class="px-3 py-1 rounded-full text-xs font-semibold select-none outline-none border transition-all {selectedTone === tone ? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]' : 'border-stone-200 text-stone-500 hover:bg-stone-50'}"
						>
							{tone}
						</button>
					{/each}
				</div>
			</div>

			<Button onclick={generatePost} disabled={isGenerating || !topic.trim()} class="w-full bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans mt-2">
				<Sparkles class="size-4 mr-2" />
				{isGenerating ? 'Drafting Post...' : 'Generate LinkedIn Post'}
			</Button>
		</CardContent>
	</Card>

	<!-- Right Side: Post Preview & Actions -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardHeader class="border-b border-stone-100 flex flex-row items-center justify-between pb-4">
			<div>
				<CardTitle class="text-base font-bold text-[#A16207] font-sans">Generated Post</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Preview and copy formatted output</CardDescription>
			</div>
			<Button onclick={handleCopy} disabled={!generatedPost} variant="outline" class="border-stone-200 hover:bg-stone-50 h-8 text-xs font-sans">
				{#if copyStatus}
					<Check class="size-3.5 text-emerald-600 mr-2" /> Copied
				{:else}
					<Copy class="size-3.5 mr-2" /> Copy All
				{/if}
			</Button>
		</CardHeader>
		<CardContent class="p-6 space-y-6">
			<!-- Main content body -->
			{#if !generatedPost && !isGenerating}
				<div class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[160px]">
					<Share2 class="size-8 text-stone-300 mb-2" />
					<p class="text-xs font-sans">Configure parameters and hit generate to draft your LinkedIn post.</p>
				</div>
			{:else if isGenerating}
				<div class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[160px] gap-2">
					<div class="size-5 border-2 border-stone-300 border-t-[#A16207] rounded-full animate-spin"></div>
					<p class="text-xs font-sans">Copilot drafting your post...</p>
				</div>
			{:else}
				<div class="space-y-4">
					<p class="text-xs leading-relaxed text-stone-800 font-sans whitespace-pre-wrap">
						{generatedPost}
					</p>

					<!-- Hashtag Area -->
					<div class="border-t border-stone-100 pt-4">
						<span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider block mb-2 font-sans">Suggested Hashtags</span>
						<div class="flex flex-wrap gap-1.5">
							{#each hashtags as tag}
								<Badge variant="secondary" class="bg-stone-50 border border-stone-200 text-stone-600 text-[10px] font-sans hover:bg-stone-100 cursor-pointer">
									#{tag}
								</Badge>
							{/each}
						</div>
					</div>
				</div>
			{/if}
		</CardContent>
	</Card>
</div>
