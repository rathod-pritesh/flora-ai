<script>
	import { appState } from "$lib/states/app.svelte.js";
	import { authStore, logout } from "$lib/stores/auth.svelte.js";
	import { Menu, User, Settings, LogOut } from "lucide-svelte";
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
	import { toast } from "svelte-sonner";

	import { goto } from "$app/navigation";

	function navigateSettings() {
		goto("/settings");
	}

	async function handleLogOut() {
		logout();
		toast.success('Logged out successfully');
		goto('/')
	}
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
					<AvatarFallback class="bg-stone-100 text-stone-650 hover:bg-stone-200 text-sm font-semibold flex items-center justify-center">
						<User class="size-4 shrink-0" />
					</AvatarFallback>
				</Avatar>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end" class="w-56 bg-white border border-stone-200 shadow-lg rounded-md p-1">
				<DropdownMenuLabel class="px-2 py-1.5 text-sm font-semibold text-stone-950 font-sans">
					My Account
				</DropdownMenuLabel>
				<DropdownMenuSeparator class="my-1 border-t border-stone-100" />
				<DropdownMenuGroup>
					<DropdownMenuItem onclick={navigateSettings} class="flex items-center gap-2 px-2 py-1.5 text-sm text-stone-700 hover:bg-stone-50 hover:text-stone-900 rounded-sm cursor-pointer outline-none font-sans">
						<Settings class="size-4" />
						Settings
					</DropdownMenuItem>
					<DropdownMenuSeparator class="my-1 border-t border-stone-100" />
					<DropdownMenuItem onclick={handleLogOut} class="flex items-center gap-2 px-2 py-1.5 text-sm text-red-600 hover:bg-red-50 hover:text-red-700 rounded-sm cursor-pointer outline-none font-sans">
						<LogOut class="size-4" />
						Log Out
					</DropdownMenuItem>
				</DropdownMenuGroup>
			</DropdownMenuContent>
		</DropdownMenu>
	</div>
</header>
