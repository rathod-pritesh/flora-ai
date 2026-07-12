<script>
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { Card, CardContent } from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { History, Search, Copy, Check, Sparkles, Languages, Share2, Code } from 'lucide-svelte';
	import { getHistory } from "$lib/services/auth"

	const apiBase = env.PUBLIC_API_URL || 'http://127.0.0.1:8000';

	let searchQuery = $state('');
	let selectedFilter = $state('All');
	let copyId = $state(null);

	let items = $state([]);
	let loading = $state(true);
	let errorMessage = $state('');

	const filters = ['All', 'Chat', 'Grammar', 'LinkedIn', 'Code Explainer'];
	const timeGroups = ['Today', 'Yesterday', 'Last 7 Days', 'Older'];

	// Get icon class and styles mapping
	function getCategoryDetails(category) {
		const normalized = (category || '').toLowerCase();
		if (normalized === 'grammar') {
			return { icon: Languages, color: 'text-[#C2410C]', bg: 'bg-[#C2410C]/10', label: 'Grammar' };
		} else if (normalized === 'linkedin') {
			return { icon: Share2, color: 'text-[#C2410C]', bg: 'bg-[#C2410C]/10', label: 'LinkedIn' };
		} else if (normalized === 'code-explainer') {
			return { icon: Code, color: 'text-stone-600', bg: 'bg-stone-100', label: 'Code Explainer' };
		} else {
			return { icon: Sparkles, color: 'text-[#A16207]', bg: 'bg-[#A16207]/10', label: 'Chat' };
		}
	}

	async function fetchHistory() {
		loading = true;
		errorMessage = '';

		try {
			const data = await getHistory();

			items = Array.isArray(data) ? data : [];
		} catch (error) {
			console.error('History fetch failed:', error);

			errorMessage = error?.message || 'Unable to load history. Please try again.';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchHistory();
	});

	const filteredItems = $derived(
		items.filter((item) => {
			const queryMatch = (item.title || item.input_text || '')
				.toLowerCase()
				.includes(searchQuery.toLowerCase());
			const resultMatch = (item.output_text || '')
				.toLowerCase()
				.includes(searchQuery.toLowerCase());
			const matchesSearch = queryMatch || resultMatch;

			let matchesFilter = false;
			if (selectedFilter === 'All') {
				matchesFilter = true;
			} else {
				const itemCategory = (item.category || '').toLowerCase();
				const selectedLower = selectedFilter.toLowerCase().replace(' ', '-');
				matchesFilter = itemCategory === selectedLower;
			}

			return matchesSearch && matchesFilter;
		})
	);

	function getTimeGroup(dateStr) {
		if (!dateStr) return 'Older';
		const date = new Date(dateStr);
		const now = new Date();

		const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
		const yesterday = new Date(today);
		yesterday.setDate(yesterday.getDate() - 1);

		const sevenDaysAgo = new Date(today);
		sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

		const compareDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

		if (compareDate.getTime() === today.getTime()) {
			return 'Today';
		} else if (compareDate.getTime() === yesterday.getTime()) {
			return 'Yesterday';
		} else if (compareDate.getTime() >= sevenDaysAgo.getTime()) {
			return 'Last 7 Days';
		} else {
			return 'Older';
		}
	}

	function formatDisplayDate(dateStr) {
		if (!dateStr) return '';
		const date = new Date(dateStr);
		return date.toLocaleString('en-US', {
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			hour12: true
		});
	}

	function handleCopy(id, text) {
		navigator.clipboard.writeText(text || '');
		copyId = id;
		setTimeout(() => (copyId = null), 1500);
	}
</script>

<div class="space-y-6">
	<!-- Filters Card -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardContent class="p-4 flex flex-col gap-4">
			<div class="relative">
				<Search class="absolute left-3 top-3 size-4 text-stone-400 shrink-0" />
				<Input
					bind:value={searchQuery}
					placeholder="Search history content..."
					class="pl-9 bg-white border-stone-200 text-xs font-sans h-10"
				/>
			</div>
			<div class="flex flex-wrap gap-2">
				{#each filters as filter}
					<button
						onclick={() => (selectedFilter = filter)}
						class="px-3 py-1 rounded-full text-xs font-semibold select-none outline-none border transition-all cursor-pointer {selectedFilter ===
						filter
							? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]'
							: 'border-stone-200 text-stone-500 hover:bg-stone-50'}"
					>
						{filter}
					</button>
				{/each}
			</div>
		</CardContent>
	</Card>

	<!-- Grouped History list -->
	<div class="space-y-8">
		{#if loading}
			<div
				class="flex flex-col items-center justify-center p-12 text-center text-stone-400 bg-white border border-stone-200 rounded-xl min-h-[200px]"
			>
				<div
					class="size-6 border-2 border-[#A16207] border-t-transparent rounded-full animate-spin mb-2"
				></div>
				<p class="text-xs font-sans">Retrieving query history...</p>
			</div>
		{:else}
			{#if errorMessage}
				<div
					class="p-4 bg-red-50 text-red-700 text-xs rounded-xl border border-red-200 font-medium"
				>
					⚠️ {errorMessage}
				</div>
			{/if}

			{#each timeGroups as group}
				{@const groupItems = filteredItems.filter(
					(item) => getTimeGroup(item.created_at) === group
				)}
				{#if groupItems.length > 0}
					<div class="space-y-3">
						<h3 class="text-xs font-bold text-stone-400 font-sans uppercase tracking-wider pl-1">
							{group}
						</h3>
						<div class="space-y-4">
							{#each groupItems as item}
								{@const cat = getCategoryDetails(item.category)}
								<Card class="bg-white border-stone-200 shadow-xs">
									<CardContent class="p-5 flex items-start gap-4">
										<div class="p-2 rounded-lg {cat.bg} {cat.color} shrink-0 mt-0.5">
											<cat.icon class="size-4 shrink-0" />
										</div>
										<div class="flex-1 min-w-0 space-y-3">
											<div class="flex justify-between items-start gap-4">
												<div class="flex items-center gap-2">
													<Badge
														variant="outline"
														class="text-[9px] font-sans text-stone-500 uppercase tracking-wider"
														>{cat.label}</Badge
													>
													<span class="text-[10px] text-stone-400 font-sans"
														>{formatDisplayDate(item.created_at)}</span
													>
												</div>
												<Button
													onclick={() => handleCopy(item.id, item.output_text)}
													variant="outline"
													class="border-stone-200 hover:bg-stone-50 h-7 px-2.5 text-[10px] font-sans cursor-pointer"
												>
													{#if copyId === item.id}
														<Check class="size-3 text-emerald-600 mr-1" /> Copied
													{:else}
														<Copy class="size-3 mr-1" /> Copy Output
													{/if}
												</Button>
											</div>
											<div class="text-xs font-sans leading-relaxed space-y-2">
												<p class="font-bold text-stone-900">{item.title || 'Untitled Query'}</p>
												<div class="bg-stone-50 border border-stone-150 rounded-lg p-3 space-y-1">
													<span
														class="block text-[8px] font-bold text-stone-400 uppercase tracking-wider font-sans"
														>Input Prompt</span
													>
													<p class="text-stone-650 whitespace-pre-wrap text-[11px] font-sans">
														{item.input_text || ''}
													</p>
												</div>
												<div class="bg-white border border-stone-200 rounded-lg p-3 space-y-1">
													<span
														class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans"
														>Output Response</span
													>
													<p class="text-stone-800 whitespace-pre-wrap text-[11px] font-sans">
														{item.output_text || ''}
													</p>
												</div>
											</div>
										</div>
									</CardContent>
								</Card>
							{/each}
						</div>
					</div>
				{/if}
			{/each}

			{#if filteredItems.length === 0}
				<div
					class="flex flex-col items-center justify-center p-8 text-center text-stone-400 bg-white border border-stone-200 rounded-xl min-h-[160px]"
				>
					<History class="size-8 text-stone-300 mb-2" />
					<p class="text-xs font-sans">No matching history entries found.</p>
				</div>
			{/if}
		{/if}
	</div>
</div>
