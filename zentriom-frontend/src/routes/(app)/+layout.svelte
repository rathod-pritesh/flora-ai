<script>
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import { appState } from "$lib/states/app.svelte.js";
	import Sidebar from "$lib/components/shared/Sidebar.svelte";
	import Header from "$lib/components/shared/Header.svelte";
	import { Sheet, SheetContent } from "$lib/components/ui/sheet/index.js";

	let { children } = $props();

	// Guard route: if user is not authenticated, redirect to landing page auth UI
	$effect(() => {
		if (!appState.user || !appState.user.name) {
			if (typeof window !== 'undefined') {
				goto("/?showAuth=true");
			}
		}
	});

	$effect(() => {
		const path = $page.url.pathname;
		appState.currentRoute = path;
		const titles = {
			"/dashboard": "Chat",
			"/settings": "Settings",
			"/grammar": "Grammar Assistant",
			"/linkedin": "LinkedIn Generator",
			"/code-explainer": "Code Explanation",
			"/bug-fixer": "Bug Fix Assistant",
			"/jobs": "Job Discovery",
			"/history": "History"
		};
		appState.pageTitle = titles[path] || "Zentriom AI";
	});
</script>

<div class="flex h-screen w-screen overflow-hidden bg-background text-foreground">
	<!-- Desktop Sidebar -->
	<div class="hidden lg:block h-full shrink-0 border-r border-border">
		<Sidebar />
	</div>

	<!-- Mobile Sidebar Drawer -->
	{#if appState.mobileSidebarOpen}
		<Sheet bind:open={appState.mobileSidebarOpen}>
			<SheetContent side="left" class="w-[280px] p-0 bg-[#1C1917] border-stone-800">
				<Sidebar />
			</SheetContent>
		</Sheet>
	{/if}

	<!-- Main Workspace Frame -->
	<div class="flex flex-1 flex-col overflow-hidden">
		<Header />
		<main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 bg-background">
			{@render children?.()}
		</main>
	</div>
</div>
