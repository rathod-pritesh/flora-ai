<script>
	import { page } from "$app/stores";
	import { appState } from "$lib/states/app.svelte.js";
	import {
		LayoutDashboard,
		Sparkles,
		Languages,
		Share2,
		Code,
		Wrench,
		Briefcase,
		History,
		User,
		LogOut,
		ChevronLeft,
		ChevronRight
	} from "lucide-svelte";

	let { onNavItemClick = null } = $props();

	const navItems = [
		{ name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
		{ name: "Workspace", path: "/workspace", icon: Sparkles },
		{ name: "Grammar", path: "/grammar", icon: Languages },
		{ name: "LinkedIn", path: "/linkedin", icon: Share2 },
		{ name: "Code Explain", path: "/code-explainer", icon: Code },
		{ name: "Bug Fix", path: "/bug-fixer", icon: Wrench },
		{ name: "Jobs", path: "/jobs", icon: Briefcase },
		{ name: "History", path: "/history", icon: History },
		{ name: "Profile", path: "/profile", icon: User }
	];
</script>

<div class="flex h-full flex-col justify-between bg-[#2D2926] text-[#F8F7F4] transition-all duration-300 {appState.sidebarCollapsed ? 'w-16' : 'w-64'}">
	<div>
		<!-- Brand Header -->
		<div class="flex h-16 items-center px-4 border-b border-[#3E3A36] justify-center lg:justify-start gap-3">
			{#if appState.sidebarCollapsed}
				<img src="/zentriom_logo_for_light_theme.png" class="size-11 object-contain" alt="Zentriom" />
			{:else}
				<div class="flex items-center gap-3">
					<img src="/zentriom_logo_for_light_theme.png" class="size-11 object-contain" alt="Zentriom" />
					<span class="text-xl font-bold tracking-tight text-[#F8F7F4] font-sans">Zentriom</span>
				</div>
			{/if}
		</div>

		<!-- Nav Items -->
		<nav class="flex-1 space-y-1 px-2 py-4">
			{#each navItems as item}
				{@const isActive = $page.url.pathname === item.path}
				<a
					href={item.path}
					onclick={() => {
						appState.mobileSidebarOpen = false;
						if (onNavItemClick) onNavItemClick();
					}}
					class="w-full flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-all outline-none select-none text-stone-400 hover:bg-[#3E3A36]/50 hover:text-white {isActive ? 'bg-[#A16207]/20 text-white border-l-2 border-[#A16207]' : ''} {appState.sidebarCollapsed ? 'justify-center px-0' : ''}"
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

	<!-- Footer / Toggle -->
	<div class="p-2 border-t border-[#3E3A36] flex flex-col gap-1">
		{#if !appState.sidebarCollapsed}
			<div class="px-3 py-2 text-[10px] text-stone-500 font-sans leading-tight">
				<p>Built with IBM Granite & LangGraph</p>
				<p class="mt-0.5 text-stone-600">Version 1.0</p>
			</div>
		{:else}
			<div class="text-center text-[10px] text-stone-500 font-mono py-2" title="Built with IBM Granite & LangGraph">
				IG
			</div>
		{/if}
		
		<button
			onclick={() => appState.sidebarCollapsed = !appState.sidebarCollapsed}
			class="hidden lg:flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-stone-500 hover:text-white justify-center outline-none select-none"
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
