<script>
	import { authStore } from "$lib/stores/auth.svelte.js";
	import { themeStore } from "$lib/stores/theme.svelte.js";
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card/index.js";
	import { Badge } from "$lib/components/ui/badge/index.js";
	import { UserX } from "lucide-svelte";
</script>

<div class="max-w-4xl mx-auto space-y-6 text-foreground">
	<!-- Account Information -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Account Information</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans">Your Zentriom profile and login credentials</CardDescription>
		</CardHeader>
		<CardContent class="p-6">
			{#if !authStore.user}
				<div class="flex items-center gap-2 text-muted-foreground text-xs font-sans py-2">
					<div class="size-4 border-2 border-[#A16207] border-t-transparent rounded-full animate-spin"></div>
					<span>Loading account details...</span>
				</div>
			{:else}
				<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
					<div>
						<span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider font-sans">Full Name</span>
						<p class="text-xs font-bold text-foreground font-sans mt-1">{authStore.user.name || "N/A"}</p>
					</div>
					<div>
						<span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider font-sans">Email Address</span>
						<p class="text-xs font-semibold text-muted-foreground font-sans mt-1">{authStore.user.email || "N/A"}</p>
					</div>
					<div>
						<span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider font-sans">Account Status</span>
						<div class="mt-1">
							<Badge class="bg-emerald-55 text-emerald-700 border-emerald-200 text-[9px] uppercase tracking-wider font-sans">
								Active
							</Badge>
						</div>
					</div>
				</div>
			{/if}
		</CardContent>
	</Card>

	<!-- Visual Theme Configuration -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Visual Theme</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans">Choose how Zentriom interface looks on your browser</CardDescription>
		</CardHeader>
		<CardContent class="p-6">
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
				<button
					onclick={() => themeStore.setTheme("light")}
					class="p-4 rounded-xl border text-left flex flex-col justify-between h-24 transition-all cursor-pointer outline-none
						{themeStore.theme === 'light' ? 'border-[#A16207] bg-[#A16207]/5' : 'border-border hover:bg-muted text-foreground'}"
				>
					<span class="text-xs font-bold text-foreground font-sans">Light Mode</span>
					<span class="text-[10px] text-muted-foreground font-sans">Standard default theme</span>
				</button>

				<button
					onclick={() => themeStore.setTheme("dark")}
					class="p-4 rounded-xl border text-left flex flex-col justify-between h-24 transition-all cursor-pointer outline-none
						{themeStore.theme === 'dark' ? 'border-[#A16207] bg-[#A16207]/5' : 'border-border hover:bg-muted text-foreground'}"
				>
					<span class="text-xs font-bold text-foreground font-sans">Dark Mode</span>
					<span class="text-[10px] text-muted-foreground font-sans">High contrast night theme</span>
				</button>

				<button
					onclick={() => themeStore.setTheme("system")}
					class="p-4 rounded-xl border text-left flex flex-col justify-between h-24 transition-all cursor-pointer outline-none
						{themeStore.theme === 'system' ? 'border-[#A16207] bg-[#A16207]/5' : 'border-border hover:bg-muted text-foreground'}"
				>
					<span class="text-xs font-bold text-foreground font-sans">System Default</span>
					<span class="text-[10px] text-muted-foreground font-sans">Syncs with operating system</span>
				</button>
			</div>
		</CardContent>
	</Card>

	<!-- AI Model Configuration -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">AI Configuration</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans">Configuration settings for AI model capabilities</CardDescription>
		</CardHeader>
		<CardContent class="p-6">
			<div class="space-y-4">
				<div class="p-4 rounded-xl border border-[#A16207]/30 bg-[#A16207]/5 text-left flex items-start gap-4">
					<div class="mt-0.5 shrink-0 flex items-center justify-center size-5 rounded-full border border-[#A16207]/30 bg-card">
						<div class="size-2.5 rounded-full bg-[#A16207]"></div>
					</div>
					<div class="flex-1 min-w-0">
						<div class="flex flex-wrap items-center justify-between gap-2">
							<h4 class="text-xs font-bold text-foreground font-sans flex items-center gap-2">
								IBM Granite 3.0 (8B) 
								<span class="bg-[#A16207]/10 text-[#A16207] text-[8px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-full">Active</span>
							</h4>
							<span class="text-[9px] text-emerald-600 font-semibold uppercase tracking-wider flex items-center gap-1">
								<span class="size-1.5 rounded-full bg-emerald-500"></span> Connected
							</span>
						</div>
						<p class="text-[10px] text-muted-foreground font-sans mt-1">Locally optimized models providing secure text completions, explanation patterns, and programming outputs.</p>
					</div>
				</div>
				
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-border">
					<div>
						<span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider font-sans">AI Service Provider</span>
						<p class="text-xs font-bold text-foreground font-sans mt-1">IBM Watsonx</p>
					</div>
					<div>
						<span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider font-sans">Model Parameter Size</span>
						<p class="text-xs font-bold text-foreground font-sans mt-1">8 Billion Parameters</p>
					</div>
				</div>
			</div>
		</CardContent>
	</Card>

	<!-- Workspace Management -->
	<Card class="bg-card border-border shadow-xs">
		<CardHeader class="border-b border-border">
			<CardTitle class="text-base font-bold text-foreground font-sans">Workspace Management</CardTitle>
			<CardDescription class="text-xs text-muted-foreground font-sans">Manage your workspace history and account deletion settings</CardDescription>
		</CardHeader>
		<CardContent class="p-6">
			<div class="w-full">
				<div class="relative p-4 rounded-xl border border-border bg-muted/50 opacity-70 select-none">
					<div class="absolute top-3 right-3 bg-muted text-muted-foreground border border-border text-[8px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full font-sans">
						UNDER DEVELOPMENT
					</div>
					<div class="p-2.5 rounded-lg bg-muted text-muted-foreground w-fit mb-3">
						<UserX class="size-4 shrink-0" />
					</div>
					<h4 class="text-xs font-bold text-muted-foreground font-sans">Delete Account</h4>
					<p class="text-[10px] text-muted-foreground font-sans mt-1">Permanently closes your account and removes all related user files.</p>
				</div>
			</div>
		</CardContent>
	</Card>
</div>
