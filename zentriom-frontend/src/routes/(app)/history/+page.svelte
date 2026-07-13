<script>
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { Card, CardContent } from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { History, Search, Copy, Check, Sparkles, Languages, Share2, Code, Trash2 } from 'lucide-svelte';
	import { getHistory, deleteHistory, clearHistory } from "$lib/services/auth"
	import { API_URL } from '$lib/config/api';
	import { fa } from 'zod/locales';
	import { toast } from 'svelte-sonner';

	let searchQuery = $state('');
	let selectedFilter = $state('all');
	let copyId = $state(null);
	let expandedState = $state({}); // card.id -> boolean

	let items = $state([]);
	let loading = $state(true);
	let errorMessage = $state('');

	let showDeleteConfirm = $state(false);
	let itemToDelete = $state(null);
	let isDeleting = $state(false);

	let showClearConfirm = $state(false);
	let isClearing = $state(false);

	const filters = [
		{ label: 'All', value: 'all' },
		{ label: 'Chat', value: 'chat' },
		{ label: 'Grammar', value: 'grammar' },
		{ label: 'LinkedIn', value: 'linkedin' },
		{ label: 'Code Explainer', value: 'code_explainer' }
	];
	const timeGroups = ['Today', 'Yesterday', 'Last 7 Days', 'Older'];

	function toggleExpand(id) {
		expandedState[id] = !expandedState[id];
	}

	function handleDeleteClick(item) {
		itemToDelete = item;
		showDeleteConfirm = true;
	}

	async function confirmDelete() {
		if (!itemToDelete) return;

		isDeleting = true;
		
		try {
			await deleteHistory(itemToDelete.id);

			items = items.filter(
				(item) => item.id !== itemToDelete.id
			);

			toast.success('History entry deleted.');
			showDeleteConfirm = false;
			itemToDelete = null;
		} catch (error) {
			console.error(error);
			toast.error('Failed to delete history entry.');
		} finally {
			isDeleting = false;
		}
	}

	function handleClearAllClick() {
		showClearConfirm = true;
	}

	async function confirmClearAll() {
		isClearing = true;
		
		try {
			await clearHistory();

			items = [];

			toast.success('All history cleared.');
			showClearConfirm = false;
		} catch (error) {
			console.error(error);
			toast.error('Failed to clear history.');
		} finally {
			isClearing = false;
		}
	}

	// Get icon class and styles mapping
	function getCategoryDetails(category) {
		const normalized = (category || '').toLowerCase();
		if (normalized === 'grammar') {
			return { icon: Languages, color: 'text-[#C2410C]', bg: 'bg-[#C2410C]/10', label: 'Grammar' };
		} else if (normalized === 'linkedin') {
			return { icon: Share2, color: 'text-[#C2410C]', bg: 'bg-[#C2410C]/10', label: 'LinkedIn' };
		} else if (normalized === 'code_explainer') {
			return { icon: Code, color: 'text-foreground', bg: 'bg-muted', label: 'Code Explainer' };
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
			toast.error('Unable to load history.');
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
			if (selectedFilter === 'all') {
				matchesFilter = true;
			} else {
				const itemCategory = (item.category || '').toLowerCase();
				matchesFilter = itemCategory === selectedFilter;
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

<div class="space-y-6 text-foreground">
	<!-- Page Header with Clear All Button -->
	<div class="flex justify-between items-center select-none pl-1 flex-wrap gap-4">
		<div>
			<h1 class="text-xl font-bold font-sans text-foreground">Activity History</h1>
			<p class="text-xs text-muted-foreground font-sans">Review and manage your past AI logs</p>
		</div>
		<Button
			variant="outline"
			class="border-red-200 text-red-600 hover:bg-red-50 dark:border-red-900/30 dark:text-red-400 dark:hover:bg-red-500/10 font-sans text-xs h-9 cursor-pointer select-none"
			onclick={handleClearAllClick}
			disabled={filteredItems.length === 0}
		>
			Clear All History
		</Button>
	</div>

	<!-- Filters Card -->
	<Card class="bg-card border-border shadow-xs">
		<CardContent class="p-4 flex flex-col gap-4">
			<div class="relative">
				<Search class="absolute left-3 top-3 size-4 text-muted-foreground shrink-0" />
				<Input
					bind:value={searchQuery}
					placeholder="Search history content..."
					class="pl-9 bg-card border-border text-xs font-sans h-10"
				/>
			</div>
			<div class="flex flex-wrap gap-2">
				{#each filters as filter}
					<button
						onclick={() => (selectedFilter = filter.value)}
						class="px-3 py-1 rounded-full text-xs font-semibold select-none outline-none border transition-all cursor-pointer {selectedFilter === filter.value
							? 'bg-[#A16207]/10 border-[#A16207] text-[#A16207]'
							: 'border-border text-muted-foreground hover:bg-muted'}"
					>
						{filter.label}
					</button>
				{/each}
			</div>
		</CardContent>
	</Card>

	<!-- Grouped History list -->
	<div class="space-y-8">
		{#if loading}
			<div
				class="flex flex-col items-center justify-center p-12 text-center text-muted-foreground bg-card border border-border rounded-xl min-h-[200px]"
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
						<h3 class="text-xs font-bold text-muted-foreground font-sans uppercase tracking-wider pl-1">
							{group}
						</h3>
						<div class="space-y-4">
							{#each groupItems as item}
								{@const cat = getCategoryDetails(item.category)}
								<Card class="bg-card border-border shadow-xs">
									<CardContent class="p-5 flex items-start gap-4">
										<div class="p-2 rounded-lg {cat.bg} {cat.color} shrink-0 mt-0.5 select-none">
											<cat.icon class="size-4 shrink-0" />
										</div>
										<div class="flex-1 min-w-0 space-y-3">
											<div class="flex justify-between items-start gap-4 flex-wrap sm:flex-nowrap">
												<div class="flex items-center gap-2">
													<Badge
														variant="outline"
														class="text-[9px] font-sans text-muted-foreground border-border uppercase tracking-wider bg-card select-none"
														>{cat.label}</Badge
													>
													<span class="text-[10px] text-muted-foreground font-sans select-none"
														>{formatDisplayDate(item.created_at)}</span
													>
												</div>
												<div class="flex items-center gap-2 select-none shrink-0">
													<Button
														onclick={() => toggleExpand(item.id)}
														variant="outline"
														class="border-border hover:bg-muted h-7 px-2.5 text-[10px] font-sans cursor-pointer bg-card text-foreground"
													>
														{expandedState[item.id] ? 'Collapse' : 'Expand'}
													</Button>
													<Button
														onclick={() => handleCopy(item.id, item.output_text)}
														variant="outline"
														class="border-border hover:bg-muted h-7 px-2.5 text-[10px] font-sans cursor-pointer bg-card text-foreground"
													>
														{#if copyId === item.id}
															<Check class="size-3 text-emerald-600 mr-1" /> Copied
														{:else}
															<Copy class="size-3 mr-1" /> Copy Output
														{/if}
													</Button>
													<Button
														onclick={() => handleDeleteClick(item)}
														variant="outline"
														class="border-border hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-500/10 dark:hover:text-red-400 h-7 w-7 p-0 flex items-center justify-center cursor-pointer bg-card text-muted-foreground"
													>
														<Trash2 class="size-3.5" />
													</Button>
												</div>
											</div>
											
											<!-- Category-Specific Layout -->
											<div class="text-xs font-sans leading-relaxed space-y-2">
												{#if item.category === 'chat'}
													<p class="font-bold text-foreground">{item.title || 'Untitled Chat'}</p>
													<div class="bg-muted/50 border border-border rounded-lg p-3 space-y-1">
														<span class="block text-[8px] font-bold text-muted-foreground uppercase tracking-wider font-sans select-none">Input Prompt</span>
														<p class="text-muted-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-2'}">
															{item.input_text || ''}
														</p>
													</div>
													<div class="bg-card border border-border rounded-lg p-3 space-y-1">
														<div class="flex items-center gap-1.5 mb-1 select-none">
															<img src="/zentriom_logo_for_dark_theme.png" class="size-3.5 object-contain" alt="Zentriom Logo" />
															<span class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans">Output Response</span>
														</div>
														<p class="text-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-3'}">
															{item.output_text || ''}
														</p>
													</div>
												{:else if item.category === 'grammar'}
													<p class="font-bold text-foreground">Grammar Correction</p>
													<div class="bg-muted/50 border border-border rounded-lg p-3 space-y-1">
														<span class="block text-[8px] font-bold text-muted-foreground uppercase tracking-wider font-sans select-none">Original Text</span>
														<p class="text-muted-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-2'}">
															{item.input_text || ''}
														</p>
													</div>
													<div class="bg-card border border-border rounded-lg p-3 space-y-1">
														<div class="flex items-center gap-1.5 mb-1 select-none">
															<img src="/zentriom_logo_for_dark_theme.png" class="size-3.5 object-contain" alt="Zentriom Logo" />
															<span class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans">Corrected Text</span>
														</div>
														<p class="text-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-3'}">
															{item.output_text || ''}
														</p>
													</div>
												{:else if item.category === 'linkedin'}
													<p class="font-bold text-foreground">{item.title || 'Untitled Post'}</p>
													<div class="bg-card border border-border rounded-lg p-3 space-y-1">
														<div class="flex items-center gap-1.5 mb-1 select-none">
															<img src="/zentriom_logo_for_dark_theme.png" class="size-3.5 object-contain" alt="Zentriom Logo" />
															<span class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans">Generated LinkedIn Post Preview</span>
														</div>
														<p class="text-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-5'}">
															{item.output_text || ''}
														</p>
													</div>
												{:else if item.category === 'code_explainer'}
													<p class="font-bold text-foreground">{item.title || 'Code Explanation'}</p>
													<div class="bg-muted/50 border border-border rounded-lg p-3 space-y-1">
														<span class="block text-[8px] font-bold text-muted-foreground uppercase tracking-wider font-sans select-none">Code Preview</span>
														<pre class="text-muted-foreground overflow-x-auto text-[11px] font-mono p-1 bg-muted/25 rounded-md {expandedState[item.id] ? '' : 'line-clamp-2'}"><code>{item.input_text || ''}</code></pre>
													</div>
													<div class="bg-card border border-border rounded-lg p-3 space-y-1">
														<div class="flex items-center gap-1.5 mb-1 select-none">
															<img src="/zentriom_logo_for_dark_theme.png" class="size-3.5 object-contain" alt="Zentriom Logo" />
															<span class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans">Explanation Preview</span>
														</div>
														<p class="text-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-3'}">
															{item.output_text || ''}
														</p>
													</div>
												{:else}
													<p class="font-bold text-foreground">{item.title || 'Untitled Query'}</p>
													<div class="bg-muted/50 border border-border rounded-lg p-3 space-y-1">
														<span class="block text-[8px] font-bold text-muted-foreground uppercase tracking-wider font-sans select-none">Input Prompt</span>
														<p class="text-muted-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-2'}">
															{item.input_text || ''}
														</p>
													</div>
													<div class="bg-card border border-border rounded-lg p-3 space-y-1">
														<div class="flex items-center gap-1.5 mb-1 select-none">
															<img src="/zentriom_logo_for_dark_theme.png" class="size-3.5 object-contain" alt="Zentriom Logo" />
															<span class="block text-[8px] font-bold text-[#A16207] uppercase tracking-wider font-sans">Output Response</span>
														</div>
														<p class="text-foreground whitespace-pre-wrap text-[11px] font-sans {expandedState[item.id] ? '' : 'line-clamp-3'}">
															{item.output_text || ''}
														</p>
													</div>
												{/if}
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
					class="flex flex-col items-center justify-center p-8 text-center text-muted-foreground bg-card border border-border rounded-xl min-h-[160px]"
				>
					<History class="size-8 text-stone-300 mb-2" />
					<p class="text-xs font-sans">
						{#if selectedFilter === 'all'}
							No matching history entries found.
						{:else if selectedFilter === 'chat'}
							No Chat history found.
						{:else if selectedFilter === 'grammar'}
							No Grammar Correction history found.
						{:else if selectedFilter === 'linkedin'}
							No LinkedIn Post history found.
						{:else if selectedFilter === 'code_explainer'}
							No Code Explanation history found.
						{/if}
					</p>
				</div>
			{/if}
		{/if}
	</div>
</div>

<!-- Confirmation Modal for Single Delete -->
{#if showDeleteConfirm}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-fade-in">
		<div class="bg-card border border-border rounded-xl shadow-lg p-6 max-w-sm w-full space-y-4 text-foreground">
			<h3 class="text-sm font-bold font-sans">Delete History Item</h3>
			<p class="text-xs text-muted-foreground font-sans">Delete this history item?</p>
			<div class="flex justify-end gap-2 text-xs font-semibold select-none">
				<Button
					variant="outline"
					class="border-border text-foreground hover:bg-muted font-sans cursor-pointer bg-card"
					onclick={() => { showDeleteConfirm = false; itemToDelete = null; }}
					disabled={isDeleting}
				>
					Cancel
				</Button>
				<Button
					variant="destructive"
					class="bg-red-600 hover:bg-red-700 text-white font-sans cursor-pointer"
					onclick={confirmDelete}
					disabled={isDeleting}
				>
					{isDeleting ? 'Deleting...' : 'Delete'}
				</Button>
			</div>
		</div>
	</div>
{/if}

<!-- Confirmation Modal for Clear All -->
{#if showClearConfirm}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-fade-in">
		<div class="bg-card border border-border rounded-xl shadow-lg p-6 max-w-sm w-full space-y-4 text-foreground">
			<h3 class="text-sm font-bold font-sans">Clear All History</h3>
			<p class="text-xs text-muted-foreground font-sans">Delete all history records? This action cannot be undone.</p>
			<div class="flex justify-end gap-2 text-xs font-semibold select-none">
				<Button
					variant="outline"
					class="border-border text-foreground hover:bg-muted font-sans cursor-pointer bg-card"
					onclick={() => showClearConfirm = false}
					disabled={isClearing}
				>
					Cancel
				</Button>
				<Button
					variant="destructive"
					class="bg-red-600 hover:bg-red-700 text-white font-sans cursor-pointer"
					onclick={confirmClearAll}
					disabled={isClearing}
				>
					{isClearing ? 'Clearing...' : 'Clear All'}
				</Button>
			</div>
		</div>
	</div>
{/if}
