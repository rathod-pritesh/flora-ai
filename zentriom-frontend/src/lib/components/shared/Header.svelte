<script>
	import { appState } from "$lib/states/app.svelte.js";
	import { Menu, User, Settings } from "lucide-svelte";
	import { Avatar, AvatarFallback } from "$lib/components/ui/avatar/index.js";
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem,
		DropdownMenuLabel,
		DropdownMenuSeparator,
		DropdownMenuGroup
	} from "$lib/components/ui/dropdown-menu/index.js";

	import { goto } from "$app/navigation";

	function navigateProfile() {
		goto("/profile");
	}
	const getInitials = (userName) => {
		if (!userName) return "PR";
		const parts = userName.trim().split(/\s+/);
		if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
		return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
	};
</script>

<header class="flex h-16 items-center justify-between border-b border-stone-200 bg-white px-4 lg:px-6">
	<div class="flex items-center gap-4">
		<!-- Mobile Toggle -->
		<button
			onclick={() => appState.mobileSidebarOpen = true}
			class="flex size-9 items-center justify-center rounded-md border border-stone-200 text-stone-600 lg:hidden hover:bg-stone-50 select-none outline-none"
			aria-label="Toggle Sidebar Menu"
		>
			<Menu class="size-5" />
		</button>

		<!-- Page Title -->
		<h1 class="text-xl font-bold tracking-tight text-stone-900 font-sans md:text-2xl">
			{appState.pageTitle}
		</h1>
	</div>

	<div class="flex items-center gap-4">
		<!-- User Menu -->
		<DropdownMenu>
			<DropdownMenuTrigger class="rounded-full outline-none focus-visible:ring-2 focus-visible:ring-[#A16207]/50 select-none">
				<Avatar class="size-9 border border-stone-200 cursor-pointer">
					<AvatarFallback class="bg-[#A16207] text-white text-sm font-semibold font-sans">
						{getInitials(appState.user?.name)}
					</AvatarFallback>
				</Avatar>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end" class="w-56 bg-white border border-stone-200 shadow-lg rounded-md p-1">
				<DropdownMenuLabel class="px-2 py-1.5 text-sm font-semibold text-stone-950 font-sans">
					My Account
				</DropdownMenuLabel>
				<DropdownMenuSeparator class="my-1 border-t border-stone-100" />
				<DropdownMenuGroup>
					<DropdownMenuItem onclick={navigateProfile} class="flex items-center gap-2 px-2 py-1.5 text-sm text-stone-700 hover:bg-stone-50 hover:text-stone-900 rounded-sm cursor-pointer outline-none font-sans">
						<User class="size-4" />
						Profile
					</DropdownMenuItem>
					<DropdownMenuItem onclick={navigateProfile} class="flex items-center gap-2 px-2 py-1.5 text-sm text-stone-700 hover:bg-stone-50 hover:text-stone-900 rounded-sm cursor-pointer outline-none font-sans">
						<Settings class="size-4" />
						Settings
					</DropdownMenuItem>
				</DropdownMenuGroup>
			</DropdownMenuContent>
		</DropdownMenu>
	</div>
</header>
