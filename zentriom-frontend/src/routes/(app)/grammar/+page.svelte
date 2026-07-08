<script>
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Textarea } from "$lib/components/ui/textarea/index.js";
	import { Badge } from "$lib/components/ui/badge/index.js";
	import { Languages, Check, Copy, Sparkles } from "lucide-svelte";

	let sourceText = $state("I have been writing code since 5 years and it is affecting my works.");
	let correctedText = $state("");
	let isChecking = $state(false);
	let copyStatus = $state(false);

	let suggestions = $state([
		{ original: "writing code since 5 years", replacement: "writing code for 5 years", type: "grammar", desc: "Use 'for' to describe a duration." },
		{ original: "affecting my works", replacement: "affecting my work", type: "clarity", desc: "Work is typically uncountable in this context." }
	]);

	function handleCheck() {
		if (!sourceText.trim()) return;
		isChecking = true;
		
		setTimeout(() => {
			correctedText = sourceText
				.replace("writing code since 5 years", "writing code for 5 years")
				.replace("affecting my works", "affecting my work");
			isChecking = false;
		}, 800);
	}

	function applySuggestion(original, replacement) {
		sourceText = sourceText.replace(original, replacement);
		suggestions = suggestions.filter(s => s.original !== original);
		correctedText = sourceText;
	}

	function applyAll() {
		suggestions.forEach(s => {
			sourceText = sourceText.replace(s.original, s.replacement);
		});
		suggestions = [];
		correctedText = sourceText;
	}

	function handleCopy() {
		navigator.clipboard.writeText(correctedText || sourceText);
		copyStatus = true;
		setTimeout(() => copyStatus = false, 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
	<!-- Left Side: Source Input -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardHeader class="border-b border-stone-100">
			<CardTitle class="text-base font-bold text-stone-900 font-sans">Source Text</CardTitle>
			<CardDescription class="text-xs text-stone-400 font-sans">Paste or write your drafts for instant correction</CardDescription>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<Textarea
				bind:value={sourceText}
				placeholder="Paste your text here..."
				class="min-h-[160px] bg-white border-stone-200 text-xs leading-relaxed font-sans"
			/>
			<div class="flex items-center justify-between">
				<span class="text-[10px] text-stone-400 font-sans">{sourceText.length} characters</span>
				<Button onclick={handleCheck} disabled={isChecking || !sourceText.trim()} class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans">
					<Sparkles class="size-4 mr-2" />
					{isChecking ? 'Checking...' : 'Check Grammar'}
				</Button>
			</div>
		</CardContent>
	</Card>

	<!-- Right Side: Suggestions & Corrected Preview -->
	<div class="space-y-6">
		{#if suggestions.length > 0}
			<!-- Suggestions Panel -->
			<Card class="bg-white border-stone-200 shadow-xs">
				<CardHeader class="border-b border-stone-100 flex flex-row items-center justify-between pb-4">
					<div>
						<CardTitle class="text-base font-bold text-stone-900 font-sans">Suggestions</CardTitle>
						<CardDescription class="text-xs text-stone-400 font-sans">Review proposed enhancements</CardDescription>
					</div>
					<Button onclick={applyAll} variant="outline" class="border-stone-200 hover:bg-stone-50 h-8 text-xs font-sans">
						Apply All
					</Button>
				</CardHeader>
				<CardContent class="p-6 space-y-4">
					{#each suggestions as sug}
						<div class="p-3 border border-stone-200 rounded-lg space-y-2">
							<div class="flex items-center justify-between">
								<Badge variant="secondary" class="text-[10px] capitalize {sug.type === 'grammar' ? 'bg-red-50 text-red-700' : 'bg-amber-50 text-amber-700'}">
									{sug.type}
								</Badge>
								<Button onclick={() => applySuggestion(sug.original, sug.replacement)} class="bg-[#A16207]/10 hover:bg-[#A16207]/20 text-[#A16207] h-7 px-2.5 text-[10px] font-sans">
									<Check class="size-3 mr-1" /> Apply
								</Button>
							</div>
							<div class="text-xs leading-relaxed text-stone-700">
								<p class="font-sans"><span class="line-through text-red-400">{sug.original}</span> <span class="font-semibold text-emerald-600">{sug.replacement}</span></p>
								<p class="text-[10px] text-stone-400 font-sans mt-1">{sug.desc}</p>
							</div>
						</div>
					{/each}
				</CardContent>
			</Card>
		{/if}

		<!-- Corrected Preview Card -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100 flex flex-row items-center justify-between pb-4">
				<div>
					<CardTitle class="text-base font-bold text-[#A16207] font-sans">Corrected Output</CardTitle>
					<CardDescription class="text-xs text-stone-400 font-sans">Polished draft ready for submission</CardDescription>
				</div>
				<Button onclick={handleCopy} variant="outline" class="border-stone-200 hover:bg-stone-50 h-8 text-xs font-sans">
					{#if copyStatus}
						<Check class="size-3.5 text-emerald-600 mr-2" /> Copied
					{:else}
						<Copy class="size-3.5 mr-2" /> Copy Output
					{/if}
				</Button>
			</CardHeader>
			<CardContent class="p-6">
				<p class="text-xs leading-relaxed text-stone-800 font-sans min-h-[80px] whitespace-pre-wrap">
					{correctedText || sourceText}
				</p>
			</CardContent>
		</Card>
	</div>
</div>
