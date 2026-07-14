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
	import { Languages, Check, Copy, Sparkles } from 'lucide-svelte';
	import { checkGrammar } from '$lib/services/auth';
	import { toast } from 'svelte-sonner';

	let sourceText = $state('I have been writing code since 5 years and it is affecting my works.');
	let correctedText = $state('');
	let isChecking = $state(false);
	let copyStatus = $state(false);

	let suggestions = $state([
		{
			original: 'writing code since 5 years',
			replacement: 'writing code for 5 years',
			type: 'grammar',
			desc: "Use 'for' to describe a duration."
		},
		{
			original: 'affecting my works',
			replacement: 'affecting my work',
			type: 'clarity',
			desc: 'Work is typically uncountable in this context.'
		}
	]);

	async function handleCheck() {
		if (!sourceText.trim()) return;

		isChecking = true;

		try {
			const data = await checkGrammar(sourceText);

			correctedText = data.corrected_text;

			suggestions = [];
		} catch (error) {
			console.error(error);
			correctedText = 'Error while checking grammer.';
			toast.error('Unable to check grammar right now.');
		} finally {
			isChecking = false;
		}
	}

	function applySuggestion(original, replacement) {
		sourceText = sourceText.replace(original, replacement);
		suggestions = suggestions.filter((s) => s.original !== original);
		correctedText = sourceText;
	}

	function applyAll() {
		suggestions.forEach((s) => {
			sourceText = sourceText.replace(s.original, s.replacement);
		});
		suggestions = [];
		correctedText = sourceText;
	}

	function handleCopy() {
		navigator.clipboard.writeText(correctedText || sourceText);
		copyStatus = true;
		setTimeout(() => (copyStatus = false), 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start text-foreground">
	<!-- Left Side: Source Input -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Source Text</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans"
				>Paste or write your drafts for instant correction</CardDescription
			>
		</CardHeader>
		<CardContent class="p-6 space-y-4">
			<Textarea
				bind:value={sourceText}
				placeholder="Paste your text here..."
				class="min-h-[160px] bg-card border-border text-foreground text-xs leading-relaxed font-sans"
			/>
			<div class="flex items-center justify-between">
				<span class="text-[10px] text-muted-foreground font-sans"
					>{sourceText.length} characters</span
				>
				<Button
					onclick={handleCheck}
					disabled={isChecking || !sourceText.trim()}
					class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 text-xs font-sans"
				>
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
			<Card class="bg-card border-border shadow-xs">
				<CardHeader class="border-b border-border flex flex-row items-center justify-between pb-4">
					<div>
						<CardTitle class="text-base font-bold text-foreground font-sans">Suggestions</CardTitle>
						<CardDescription class="text-xs text-muted-foreground font-sans"
							>Review proposed enhancements</CardDescription
						>
					</div>
					<Button
						onclick={applyAll}
						variant="outline"
						class="border-border hover:bg-muted h-8 text-xs font-sans bg-card text-foreground"
					>
						Apply All
					</Button>
				</CardHeader>
				<CardContent class="p-6 space-y-4">
					{#each suggestions as sug}
						<div class="p-3 border border-border rounded-lg space-y-2 bg-muted/30">
							<div class="flex items-center justify-between">
								<Badge
									variant="secondary"
									class="text-[10px] capitalize {sug.type === 'grammar'
										? 'bg-red-50 text-red-700 dark:bg-red-500/10 dark:text-red-400'
										: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400'}"
								>
									{sug.type}
								</Badge>
								<Button
									onclick={() => applySuggestion(sug.original, sug.replacement)}
									class="bg-[#A16207]/10 hover:bg-[#A16207]/20 text-[#A16207] h-7 px-2.5 text-[10px] font-sans"
								>
									<Check class="size-3 mr-1" /> Apply
								</Button>
							</div>
							<div class="text-xs leading-relaxed text-foreground">
								<p class="font-sans">
									<span class="line-through text-red-400">{sug.original}</span>
									<span class="font-semibold text-emerald-600 dark:text-emerald-450"
										>{sug.replacement}</span
									>
								</p>
								<p class="text-[10px] text-muted-foreground font-sans mt-1">{sug.desc}</p>
							</div>
						</div>
					{/each}
				</CardContent>
			</Card>
		{/if}

		<!-- Corrected Preview Card -->
		<Card class="bg-card border-border shadow-xs">
			<CardHeader class="border-b border-border flex flex-row items-center justify-between pb-4">
				<div>
					<CardTitle class="text-base font-bold text-[#A16207] font-sans"
						>Corrected Output</CardTitle
					>
					<CardDescription class="text-xs text-muted-foreground font-sans"
						>Polished draft ready for submission</CardDescription
					>
				</div>
				<Button
					onclick={handleCopy}
					variant="outline"
					class="border-border hover:bg-muted h-8 text-xs font-sans bg-card text-foreground"
				>
					{#if copyStatus}
						<Check class="size-3.5 text-emerald-600 mr-2" /> Copied
					{:else}
						<Copy class="size-3.5 mr-2" /> Copy Output
					{/if}
				</Button>
			</CardHeader>
			<CardContent class="p-6">
				<p
					class="text-xs leading-relaxed text-foreground font-sans min-h-[80px] whitespace-pre-wrap"
				>
					{correctedText || sourceText}
				</p>
			</CardContent>
		</Card>
	</div>
</div>
