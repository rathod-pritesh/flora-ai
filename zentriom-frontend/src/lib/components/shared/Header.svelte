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
		toast.success('You have been signed out');
		goto('/')
	}
</script>

<header class="flex h-16 items-center justify-between border-b border-border bg-card text-foreground px-4 lg:px-6">
	<div class="flex items-center gap-4">
		<!-- Mobile Toggle -->
		<button
			onclick={() => appState.mobileSidebarOpen = true}
			class="flex size-9 items-center justify-center rounded-md border border-border text-foreground lg:hidden hover:bg-muted select-none outline-none"
			aria-label="Toggle Sidebar Menu"
		>
			<Menu class="size-5" />
		</button>

		<!-- Page Title -->
		<h1 class="text-xl font-bold tracking-tight text-foreground font-sans md:text-2xl">
			{appState.pageTitle}
		</h1>
	</div>

	<div class="flex items-center gap-4">
		<!-- User Menu -->
		<DropdownMenu>
			<DropdownMenuTrigger class="rounded-full outline-none focus-visible:ring-2 focus-visible:ring-[#A16207]/50 select-none">
				<Avatar class="size-9 border border-border cursor-pointer">
					<AvatarFallback class="bg-muted text-muted-foreground hover:bg-accent text-sm font-semibold flex items-center justify-center">
						<User class="size-4 shrink-0" />
					</AvatarFallback>
				</Avatar>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end" class="w-56 bg-card border border-border shadow-lg rounded-md p-1 text-foreground">
				<DropdownMenuLabel class="px-2 py-1.5 text-sm font-semibold text-foreground font-sans">
					My Account
				</DropdownMenuLabel>
				<DropdownMenuSeparator class="my-1 border-t border-border" />
				<DropdownMenuGroup>
					<DropdownMenuItem onclick={navigateSettings} class="flex items-center gap-2 px-2 py-1.5 text-sm text-foreground hover:bg-muted rounded-sm cursor-pointer outline-none font-sans">
						<Settings class="size-4" />
						Settings
					</DropdownMenuItem>
					<DropdownMenuSeparator class="my-1 border-t border-border" />
					<DropdownMenuItem onclick={handleLogOut} class="flex items-center gap-2 px-2 py-1.5 text-sm text-red-650 hover:bg-red-500/10 dark:hover:bg-red-500/20 rounded-sm cursor-pointer outline-none font-sans">
						<LogOut class="size-4" />
						Log Out
					</DropdownMenuItem>
				</DropdownMenuGroup>
			</DropdownMenuContent>
		</DropdownMenu>
	</div>
</header>
