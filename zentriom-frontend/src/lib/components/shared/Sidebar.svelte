<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { appState } from '$lib/states/app.svelte.js';
	import { themeStore } from '$lib/stores/theme.svelte.js';
	import { MessageSquare, History, Settings, ChevronLeft, ChevronRight, Plus } from 'lucide-svelte';

	let { onNavItemClick = null } = $props();

	const navItems = [
		{ name: 'Chat', path: '/dashboard', icon: MessageSquare },
		{ name: 'History', path: '/history', icon: History },
		{ name: 'Settings', path: '/settings', icon: Settings }
	];

	function triggerNewChat() {
		if ($page.url.pathname !== '/dashboard') {
			goto('/dashboard').then(() => {
				if (appState.onNewChat) appState.onNewChat();
			});
		} else {
			if (appState.onNewChat) appState.onNewChat();
		}
		appState.mobileSidebarOpen = false;
		if (onNavItemClick) onNavItemClick();
	}

	const isDark = $derived(
		themeStore.theme === 'dark' ||
			(themeStore.theme === 'system' &&
				typeof window !== 'undefined' &&
				window.matchMedia('(prefers-color-scheme: dark)').matches)
	);
</script>

<div
	class="flex h-full flex-col justify-between bg-sidebar text-sidebar-foreground border-r border-sidebar-border transition-all duration-300 {appState.sidebarCollapsed
		? 'w-16'
		: 'w-64'}"
>
	<div>
		<div
			class="flex h-16 items-center px-4 border-b border-sidebar-border justify-center lg:justify-start gap-3"
		>
			{#if appState.sidebarCollapsed}
				<img
					src={isDark ? '/logo.png' : '/logo2.png'}
					class="size-11 object-contain"
					alt="Zentriom"
				/>
			{:else}
				<div class="flex items-center gap-3">
					<img
						src={isDark ? '/logo.png' : '/logo2.png'}
						class="size-11 object-contain"
						alt="Zentriom"
					/>
					<span class="text-xl font-bold tracking-tight text-sidebar-foreground font-sans"
						>Zentriom</span
					>
				</div>
			{/if}
		</div>

		<div class="px-2 pt-4">
			<button
				onclick={triggerNewChat}
				class="w-full flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-all outline-none select-none border border-sidebar-border bg-sidebar-accent/30 text-sidebar-foreground hover:bg-sidebar-accent/70 hover:text-sidebar-foreground cursor-pointer {appState.sidebarCollapsed
					? 'justify-center px-0'
					: ''}"
				title="New Chat"
			>
				<Plus class="size-5 shrink-0" />
				{#if !appState.sidebarCollapsed}
					<span class="font-sans">New Chat</span>
				{/if}
			</button>
		</div>

		<nav class="flex-1 space-y-1 px-2 py-4">
			{#each navItems as item}
				{@const isActive = $page.url.pathname === item.path}
				<a
					href={item.path}
					onclick={() => {
						appState.mobileSidebarOpen = false;
						if (onNavItemClick) onNavItemClick();
					}}
					class="w-full flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-all outline-none select-none text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground {isActive
						? 'bg-sidebar-accent text-sidebar-foreground font-semibold border-l-2 border-sidebar-primary'
						: ''} {appState.sidebarCollapsed ? 'justify-center px-0' : ''}"
					title={item.name}
				>
					<item.icon class="size-5 shrink-0" />
					{#if !appState.sidebarCollapsed}
						<span class="truncate font-sans">{item.name}</span>
					{/if}
				</a>
			{/each}
		</nav>
	</div>

	<div class="p-2 border-t border-sidebar-border flex flex-col gap-1">
		{#if !appState.sidebarCollapsed}
			<div class="px-3 py-2 text-[10px] text-sidebar-foreground/60 font-sans leading-tight">
				<p>Built with IBM Granite & LangGraph</p>
				<p class="mt-0.5 text-sidebar-foreground/40">Version 1.0</p>
			</div>
		{/if}

		<button
			onclick={() => (appState.sidebarCollapsed = !appState.sidebarCollapsed)}
			class="hidden lg:flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground justify-center outline-none select-none cursor-pointer"
			title={appState.sidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
		>
			{#if appState.sidebarCollapsed}
				<ChevronRight class="size-4" />
			{:else}
				<div class="flex items-center gap-2">
					<ChevronLeft class="size-4" />
					<span class="text-xs font-sans">Collapse</span>
				</div>
			{/if}
		</button>
	</div>
</div>
