<script>
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Share2, Copy, Check, Sparkles } from 'lucide-svelte';
	import { generateLinkedInPost } from '$lib/services/auth';
	import { toast } from 'svelte-sonner';

	let postType = $state('Certificate');
	const postTypes = [
		'Certificate',
		'Project',
		'Internship',
		'Learning',
		'Achievement',
		'Open Source',
		'General'
	];

	let topic = $state('');
	let experience = $state('');
	let selectedTone = $state('Professional');
	let length = $state('Standard');

	const lengths = ['Brief', 'Standard', 'Detailed'];

	let isGenerating = $state(false);
	let generatedPost = $state('');
	let copyStatus = $state(false);

	const tones = ['Professional', 'Creative', 'Confident', 'Insightful'];

	async function generatePost() {
		if (!topic.trim() || !experience.trim()) return;
		isGenerating = true;

		try {
			const data = await generateLinkedInPost({
				post_type: postType,
				topic,
				experience,
				tone: selectedTone,
				length
			});

			generatedPost = data.post;
		} catch (error) {
			console.error(error);

			generatedPost = 'Unable to connect to backend. Please try again.';
			toast.error('Unable to generate LinkedIn post.');
		} finally {
			isGenerating = false;
		}
	}

	function handleCopy() {
		navigator.clipboard.writeText(generatedPost);

		copyStatus = true;

		setTimeout(() => {
			copyStatus = false;
		}, 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start text-foreground">
	<!-- Left Side: Prompt Builder -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Post Parameters</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans"
				>Set topics and context for your post</CardDescription
			>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<div class="space-y-1.5">
				<span class="text-xs font-semibold text-foreground block"> Post Type </span>

				<div class="flex flex-wrap gap-2">
					{#each postTypes as type}
						<button
							onclick={() => (postType = type)}
							class="px-3 py-1 rounded-full text-xs border transition-all cursor-pointer select-none outline-none
				{postType === type
								? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]'
								: 'border-border text-muted-foreground hover:bg-muted'}"
						>
							{type}
						</button>
					{/each}
				</div>
			</div>
			<!-- Topic -->
			<div class="space-y-1">
				<label for="topic" class="text-xs font-semibold text-foreground font-sans">Topic</label>
				<Textarea
					id="topic"
					bind:value={topic}
					placeholder="What is your post about?"
					class="min-h-[80px] bg-card border-border text-foreground text-xs font-sans"
				/>
			</div>

			<div class="space-y-1">
				<label for="experience" class="text-xs font-semibold text-foreground">
					Experience / Key Learning
				</label>

				<Textarea
					bind:value={experience}
					placeholder="What did you learn? What surprised you? What was difficult?"
					class="min-h-[140px] bg-card border-border text-foreground text-xs font-sans"
				/>
			</div>

			<!-- Tones -->
			<div class="space-y-1.5">
				<span class="text-xs font-semibold text-foreground font-sans block">Tone</span>
				<div class="flex flex-wrap gap-2">
					{#each tones as tone}
						<button
							onclick={() => (selectedTone = tone)}
							class="px-3 py-1 rounded-full text-xs font-semibold select-none outline-none border transition-all cursor-pointer {selectedTone ===
							tone
								? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]'
								: 'border-border text-muted-foreground hover:bg-muted'}"
						>
							{tone}
						</button>
					{/each}
				</div>
			</div>

			<div class="space-y-1.5">
				<span class="text-xs font-semibold text-foreground block"> Post Length </span>

				<div class="flex gap-2">
					{#each lengths as item}
						<button
							onclick={() => (length = item)}
							class="px-3 py-1 rounded-full text-xs border transition-all cursor-pointer select-none outline-none
				{length === item
								? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]'
								: 'border-border text-muted-foreground hover:bg-muted'}"
						>
							{item}
						</button>
					{/each}
				</div>
			</div>

			<Button
				onclick={generatePost}
				disabled={isGenerating || !topic.trim()}
				class="w-full bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans mt-2"
			>
				<Sparkles class="size-4 mr-2" />
				{isGenerating ? 'Drafting Post...' : 'Generate LinkedIn Post'}
			</Button>
		</CardContent>
	</Card>

	<!-- Right Side: Post Preview & Actions -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border flex flex-row items-center justify-between pb-4">
			<div>
				<CardTitle class="text-base font-bold text-[#A16207] font-sans">LinkedIn Draft</CardTitle>
				<CardDescription class="text-xs text-muted-foreground font-sans"
					>Preview and copy formatted output</CardDescription
				>
			</div>
			<Button
				onclick={handleCopy}
				disabled={!generatedPost}
				variant="outline"
				class="border-border hover:bg-muted h-8 text-xs font-sans bg-card text-foreground"
			>
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
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-muted-foreground min-h-[160px]"
				>
					<Share2 class="size-8 text-stone-300 mb-2" />
					<p class="text-xs font-sans">
						Configure parameters and hit generate to draft your LinkedIn post.
					</p>
				</div>
			{:else if isGenerating}
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-muted-foreground min-h-[160px] gap-2"
				>
					<div
						class="size-5 border-2 border-border border-t-[#A16207] rounded-full animate-spin"
					></div>
					<p class="text-xs font-sans">Copilot drafting your post...</p>
				</div>
			{:else}
				<div class="space-y-4">
					<p class="text-xs leading-relaxed text-foreground font-sans whitespace-pre-wrap">
						{generatedPost}
					</p>
				</div>
			{/if}
		</CardContent>
	</Card>
</div>
