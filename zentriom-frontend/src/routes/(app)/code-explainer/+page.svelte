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
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Code, Copy, Check, Sparkles } from 'lucide-svelte';
	import { explainCode } from '$lib/services/auth';

	let codeSnippet = $state('const double = (arr) => arr.map(x => x * 2);');
	let isAnalyzing = $state(false);
	let explanation = $state('');

	let detectedLanguage = $state('');

	let steps = $state([]);
	let copyStatus = $state(false);

	async function handleExplain() {
		if (!codeSnippet.trim()) return;

		isAnalyzing = true;

		try {
			const result = await explainCode(codeSnippet);

			explanation = result.explanation;
			detectedLanguage = result.language;
		} catch (err) {
			console.error(err);

			alert('Failed to explain code');
		} finally {
			isAnalyzing = false;
		}
	}

	function handleCopy() {
		const fullText = `Code:\n${codeSnippet}\n\nExplanation:\n${explanation}\n\nSteps:\n${steps.map((s) => `- ${s.title}: ${s.desc}`).join('\n')}`;
		navigator.clipboard.writeText(fullText);
		copyStatus = true;
		setTimeout(() => (copyStatus = false), 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
	<!-- Left: Code Input Card -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardHeader class="border-b border-stone-100">
			<CardTitle class="text-base font-bold text-stone-900 font-sans">Code Editor Area</CardTitle>
			<CardDescription class="text-xs text-stone-400 font-sans"
				>Input or paste code snippets to generate explanations</CardDescription
			>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<div class="relative">
				<Textarea
					bind:value={codeSnippet}
					placeholder="Paste code snippet here..."
					class="min-h-[220px] bg-stone-50 border-stone-200 text-xs font-mono p-4 leading-relaxed resize-none focus-visible:ring-1 focus-visible:ring-[#A16207]/50"
				/>

				{#if detectedLanguage}
					<div
						class="absolute bottom-3 left-3 z-10
			px-3 py-1
			rounded-full
			bg-stone-900/90
			text-white
			text-[10px] sm:text-xs
			font-medium
			backdrop-blur-sm"
					>
						{detectedLanguage}
					</div>
				{/if}
			</div>

			<div class="flex items-center justify-between">
				<span class="text-[10px] text-stone-400 font-sans"
					>{codeSnippet.split('\n').length} lines of code</span
				>
				<Button
					onclick={handleExplain}
					disabled={isAnalyzing || !codeSnippet.trim()}
					class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans"
				>
					<Sparkles class="size-4 mr-2" />
					{isAnalyzing ? 'Explaining...' : 'Explain Code'}
				</Button>
			</div>
		</CardContent>
	</Card>

	<!-- Right: Explanation Panel -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardHeader class="border-b border-stone-100 flex flex-row items-center justify-between pb-4">
			<div>
				<CardTitle class="text-base font-bold text-[#A16207] font-sans">Explanation Panel</CardTitle
				>
				<CardDescription class="text-xs text-stone-400 font-sans"
					>Structured breakdown of the snippet</CardDescription
				>
			</div>
			<Button
				onclick={handleCopy}
				disabled={!explanation}
				variant="outline"
				class="border-stone-200 hover:bg-stone-50 h-8 text-xs font-sans"
			>
				{#if copyStatus}
					<Check class="size-3.5 text-emerald-600 mr-2" /> Copied
				{:else}
					<Copy class="size-3.5 mr-2" /> Copy Breakdown
				{/if}
			</Button>
		</CardHeader>
		<CardContent class="p-6">
			{#if !explanation && !isAnalyzing}
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[180px]"
				>
					<Code class="size-8 text-stone-350 mb-2" />
					<p class="text-xs font-sans">
						Paste code on the left editor and hit explain to see step-by-step breakdown.
					</p>
				</div>
			{:else if isAnalyzing}
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[180px] gap-2"
				>
					<div
						class="size-5 border-2 border-stone-300 border-t-[#A16207] rounded-full animate-spin"
					></div>
					<p class="text-xs font-sans">Decompiling snippet architecture...</p>
				</div>
			{:else}
				<div class="space-y-4">
					<div class="p-3 bg-stone-50 border border-stone-150 rounded-lg">
						<p class="text-xs leading-relaxed text-stone-850 font-sans font-medium">
							{explanation}
						</p>
					</div>
					<div class="space-y-3">
						<span
							class="text-[10px] font-bold text-stone-400 uppercase tracking-wider block font-sans"
							>Step-by-step Explanation</span
						>
						{#each steps as step, index}
							<div class="flex gap-3">
								<span
									class="flex size-5 items-center justify-center rounded-full bg-[#A16207]/10 text-[#A16207] text-[10px] font-bold font-sans shrink-0"
									>{index + 1}</span
								>
								<div class="text-xs">
									<p class="font-bold text-stone-800 font-sans">{step.title}</p>
									<p class="text-stone-500 font-sans leading-relaxed mt-0.5">{step.desc}</p>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</CardContent>
	</Card>
</div>

<style>
	.language-badge {
		position: absolute;
		right: 12px;
		bottom: 12px;

		padding: 4px 10px;

		border-radius: 999px;

		font-size: 12px;
		font-weight: 600;

		background: rgba(255, 255, 255, 0.08);
	}
</style>
