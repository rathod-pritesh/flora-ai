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
	import { Wrench, Copy, Check, TriangleAlert, Sparkles } from 'lucide-svelte';

	let buggyCode = $state('function sum(a, b) {\n  return a - b;\n}');
	let errorLog = $state('TypeError: sum(1, 2) returned -1 instead of 3');
	let isAnalyzing = $state(false);
	let rootCause = $state('');
	let fixedCode = $state('');
	let copyStatus = $state(false);

	function analyzeBug() {
		if (!buggyCode.trim()) return;
		isAnalyzing = true;

		setTimeout(() => {
			rootCause =
				"The function is using the subtraction operator ('-') instead of the addition operator ('+'), leading to incorrect arithmetic returns.";
			fixedCode = 'function sum(a, b) {\n  // Fixed operator to addition\n  return a + b;\n}';
			isAnalyzing = false;
		}, 800);
	}

	function handleCopy() {
		navigator.clipboard.writeText(fixedCode);
		copyStatus = true;
		setTimeout(() => (copyStatus = false), 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
	<!-- Left: Inputs (Buggy Code & Error Logs) -->
	<div class="space-y-6">
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100">
				<CardTitle class="text-base font-bold text-stone-900 font-sans">Buggy Code Input</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans"
					>Paste the script containing the runtime exception</CardDescription
				>
			</CardHeader>
			<CardContent class="p-6 space-y-4">
				<Textarea
					bind:value={buggyCode}
					placeholder="Paste code containing bugs..."
					class="min-h-[120px] bg-stone-50 border-stone-200 text-xs font-mono p-4"
				/>
			</CardContent>
		</Card>

		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100">
				<CardTitle class="text-base font-bold text-stone-900 font-sans"
					>Error Logs / Stacktrace</CardTitle
				>
				<CardDescription class="text-xs text-stone-400 font-sans"
					>Paste compiler errors or logs here</CardDescription
				>
			</CardHeader>
			<CardContent class="p-6 space-y-4">
				<Textarea
					bind:value={errorLog}
					placeholder="TypeError: example is not a function..."
					class="min-h-[80px] bg-red-50/20 border-stone-200 text-xs font-mono text-red-700 p-3"
				/>
				<div class="flex items-center justify-between">
					<span class="text-[10px] text-stone-400 font-sans">Syntax diagnostics: Auto-enabled</span>
					<Button
						onclick={analyzeBug}
						disabled={isAnalyzing || !buggyCode.trim()}
						class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans"
					>
						<Wrench class="size-4 mr-2" />
						{isAnalyzing ? 'Resolving...' : 'Analyze & Fix'}
					</Button>
				</div>
			</CardContent>
		</Card>
	</div>

	<!-- Right: Results (Root Cause & Solution Code) -->
	<div class="space-y-6">
		<!-- Root Cause Panel -->
		{#if rootCause}
			<Card class="bg-white border-stone-200 shadow-xs border-l-4 border-l-[#C2410C]">
				<CardHeader class="border-b border-stone-100 pb-3">
					<div class="flex items-center gap-2">
						<TriangleAlert class="size-4 text-[#C2410C] shrink-0" />
						<CardTitle class="text-base font-bold text-[#C2410C] font-sans"
							>Root Cause Analysis</CardTitle
						>
					</div>
				</CardHeader>
				<CardContent class="p-4">
					<p class="text-xs leading-relaxed text-stone-700 font-sans font-medium">
						{rootCause}
					</p>
				</CardContent>
			</Card>
		{/if}

		<!-- Solution Code Panel -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100 flex flex-row items-center justify-between pb-4">
				<div>
					<CardTitle class="text-base font-bold text-[#A16207] font-sans"
						>Proposed Solution</CardTitle
					>
					<CardDescription class="text-xs text-stone-400 font-sans"
						>Verified compiler-compliant fix</CardDescription
					>
				</div>
				<Button
					onclick={handleCopy}
					disabled={!fixedCode}
					variant="outline"
					class="border-stone-200 hover:bg-stone-50 h-8 text-xs font-sans"
				>
					{#if copyStatus}
						<Check class="size-3.5 text-emerald-600 mr-2" /> Copied
					{:else}
						<Copy class="size-3.5 mr-2" /> Copy Fix
					{/if}
				</Button>
			</CardHeader>
			<CardContent class="p-6">
				{#if !fixedCode && !isAnalyzing}
					<div
						class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[160px]"
					>
						<Wrench class="size-8 text-stone-350 mb-2" />
						<p class="text-xs font-sans">
							Submit code inputs and stacktraces to generate solutions.
						</p>
					</div>
				{:else if isAnalyzing}
					<div
						class="flex flex-col items-center justify-center p-8 text-center text-stone-400 min-h-[160px] gap-2"
					>
						<div
							class="size-5 border-2 border-stone-300 border-t-[#A16207] rounded-full animate-spin"
						></div>
						<p class="text-xs font-sans">Synthesizing patch code...</p>
					</div>
				{:else}
					<Textarea
						readonly
						value={fixedCode}
						class="min-h-[160px] bg-[#A16207]/5 border-[#A16207]/20 text-xs font-mono text-stone-850 p-4 leading-relaxed resize-none focus-visible:ring-0"
					/>
				{/if}
			</CardContent>
		</Card>
	</div>
</div>
