<script>
	import { page } from "$app/stores";
	import { appState } from "$lib/states/app.svelte.js";
	import Sidebar from "$lib/components/shared/Sidebar.svelte";
	import Header from "$lib/components/shared/Header.svelte";
	import { Sheet, SheetContent } from "$lib/components/ui/sheet/index.js";

	let { children } = $props();

	$effect(() => {
		const path = $page.url.pathname;
		appState.currentRoute = path;
		const titles = {
			"/dashboard": "Dashboard",
			"/workspace": "AI Workspace",
			"/grammar": "Grammar Assistant",
			"/linkedin": "LinkedIn Generator",
			"/code-explainer": "Code Explanation",
			"/bug-fixer": "Bug Fix Assistant",
			"/jobs": "Job Discovery",
			"/history": "History",
			"/profile": "Profile"
		};
		appState.pageTitle = titles[path] || "Zentriom AI";
	});
</script>

<div class="flex h-screen w-screen overflow-hidden bg-[#FAFAF9]">
	<!-- Desktop Sidebar -->
	<div class="hidden lg:block h-full shrink-0 border-r border-stone-200">
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
		<main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 bg-[#FAFAF9]">
			{@render children?.()}
		</main>
	</div>
</div>
