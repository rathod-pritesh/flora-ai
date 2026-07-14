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
	import { toast } from 'svelte-sonner';

	let codeSnippet = $state(`def is_armstrong(num):
    num_str = str(num)
    n = len(num_str)
    return sum(int(digit) ** n for digit in num_str) == num`);
	let isAnalyzing = $state(false);
	let explanation = $state('');
	let detectedLanguage = $state('');
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
			toast.error('Unable to explain the code.');
		} finally {
			isAnalyzing = false;
		}
	}

	function handleCopy() {
		const fullText = `Code:\n${codeSnippet}\n\nExplanation:\n${explanation}`;
		navigator.clipboard.writeText(fullText);
		copyStatus = true;
		setTimeout(() => (copyStatus = false), 1500);
	}

	function formatMarkdown(text) {
		if (!text) return '';
		let escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		escaped = escaped.replace(
			/\*\*(.*?)\*\*/g,
			"<strong class='font-bold text-foreground'>$1</strong>"
		);
		escaped = escaped.replace(/\*(.*?)\*/g, "<em class='italic'>$1</em>");
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
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start text-foreground">
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Code Editor Area</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans"
				>Input or paste code snippets to generate explanations</CardDescription
			>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<div class="relative">
				<Textarea
					bind:value={codeSnippet}
					wrap="off"
					placeholder="Paste code snippet here..."
					class="min-h-[220px] bg-muted/40 border-border text-foreground text-xs font-mono p-4 leading-relaxed resize-none focus-visible:ring-1 focus-visible:ring-[#A16207]/50 overflow-auto whitespace-pre"
				/>

				{#if detectedLanguage}
					<div
						class="absolute bottom-3 left-3 z-10 px-3 py-1 rounded-full bg-stone-900/90 text-white text-[10px] sm:text-xs font-medium backdrop-blur-sm"
					>
						{detectedLanguage}
					</div>
				{/if}
			</div>

			<div class="flex items-center justify-between">
				<span class="text-[10px] text-muted-foreground font-sans">
					{codeSnippet.split('\n').length} lines of code
				</span>
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

	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border flex flex-row items-center justify-between pb-4">
			<div>
				<CardTitle class="text-base font-bold text-[#A16207] font-sans">Explanation Panel</CardTitle
				>
				<CardDescription class="text-xs text-muted-foreground font-sans"
					>Structured breakdown of the snippet</CardDescription
				>
			</div>
			<Button
				onclick={handleCopy}
				disabled={!explanation}
				variant="outline"
				class="border-border hover:bg-muted h-8 text-xs font-sans bg-card text-foreground"
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
					class="flex flex-col items-center justify-center p-8 text-center text-muted-foreground min-h-[180px]"
				>
					<Code class="size-8 text-stone-350 mb-2" />
					<p class="text-xs font-sans">
						Paste code on the left editor and hit explain to see its explanation.
					</p>
				</div>
			{:else if isAnalyzing}
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-muted-foreground min-h-[180px] gap-2"
				>
					<div
						class="size-5 border-2 border-border border-t-[#A16207] rounded-full animate-spin"
					></div>
					<p class="text-xs font-sans">Decompiling snippet architecture...</p>
				</div>
			{:else}
				<div class="space-y-4 max-h-[450px] overflow-y-auto pr-2">
					{#if detectedLanguage}
						<Badge
							variant="outline"
							class="text-[9px] font-sans text-muted-foreground border-border uppercase tracking-wider bg-card w-fit select-none"
						>
							{detectedLanguage}
						</Badge>
					{/if}

					{#each parseMarkdown(explanation) as block}
						{#if block.type === 'code'}
							<div
								class="my-3 rounded-lg overflow-hidden border border-border font-mono text-xs shadow-inner"
							>
								{#if block.lang}
									<div
										class="bg-muted border-b border-border px-3 py-1.5 text-[10px] text-muted-foreground font-sans font-semibold flex items-center justify-between"
									>
										<span>{block.lang.toUpperCase()}</span>
									</div>
								{/if}
								<pre
									class="bg-muted/50 p-3 overflow-auto max-h-[250px] text-foreground leading-relaxed"><code
										>{block.code}</code
									></pre>
							</div>
						{:else}
							<div
								class="whitespace-pre-wrap font-sans text-xs sm:text-sm leading-relaxed text-foreground space-y-2"
							>
								{#each block.content.split('\n') as paragraph}
									{#if paragraph.trim()}
										<p class="leading-relaxed">
											{@html formatMarkdown(paragraph)}
										</p>
									{/if}
								{/each}
							</div>
						{/if}
					{/each}
				</div>
			{/if}
		</CardContent>
	</Card>
</div>
