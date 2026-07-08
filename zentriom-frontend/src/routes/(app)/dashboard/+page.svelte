<script>
	import { appState } from "$lib/states/app.svelte.js";
	import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "$lib/components/ui/card/index.js";
	import { Sparkles, Languages, Share2, Briefcase, History } from "lucide-svelte";

	const stats = [
		{ title: "AI Completions", value: "32", icon: Sparkles, color: "text-[#A16207]", bg: "bg-[#A16207]/10" },
		{ title: "Grammar Fixes", value: "148", icon: Languages, color: "text-[#C2410C]", bg: "bg-[#C2410C]/10" },
		{ title: "LinkedIn Shares", value: "12", icon: Share2, color: "text-[#A16207]", bg: "bg-[#A16207]/10" },
		{ title: "Job Matches", value: "85%", icon: Briefcase, color: "text-stone-700", bg: "bg-stone-100" }
	];

	const activities = [
		{ text: "Drafted LinkedIn post on Tech Trends", time: "2 hours ago", type: "Share2" },
		{ text: "Checked resume grammar corrections", time: "5 hours ago", type: "Languages" },
		{ text: "Explained React to Svelte migration code", time: "Yesterday", type: "Code" },
		{ text: "Fixed memory leak bug in Express server", time: "2 days ago", type: "Wrench" }
	];

	const quickActions = [
		{ name: "AI Workspace", path: "/workspace", desc: "Start a new drafting canvas", icon: Sparkles },
		{ name: "Grammar Fixer", path: "/grammar", desc: "Improve clarity and correctness", icon: Languages },
		{ name: "LinkedIn Post", path: "/linkedin", desc: "Generate professional posts", icon: Share2 },
		{ name: "Explain Code", path: "/code-explainer", desc: "Breakdown complex snippets", icon: Sparkles }
	];
</script>

<div class="space-y-6">
	<!-- Welcome Section -->
	<div class="rounded-xl border border-stone-200 bg-white p-6 shadow-xs">
		<div class="max-w-2xl">
			<h2 class="text-2xl font-bold tracking-tight text-stone-900 font-sans sm:text-3xl">
				Good Morning, {appState.user?.name ? appState.user.name.split(' ')[0] : 'Developer'} 👋
			</h2>
			<p class="mt-2 text-stone-500 font-sans text-sm leading-relaxed md:text-base">
				Your AI Career Copilot is ready. Draft copy, refactor system code, or check matching job markets from your local environment.
			</p>
		</div>
	</div>

	<!-- Productivity Overview Stats -->
	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
		{#each stats as stat}
			<Card class="bg-white border-stone-200 shadow-xs">
				<CardContent class="p-5 flex items-center justify-between">
					<div class="space-y-1">
						<p class="text-xs font-medium text-stone-400 uppercase tracking-wider font-sans">{stat.title}</p>
						<p class="text-2xl font-bold text-stone-900 font-sans">{stat.value}</p>
					</div>
					<div class="p-2.5 rounded-lg {stat.bg} {stat.color}">
						<stat.icon class="size-5 shrink-0" />
					</div>
				</CardContent>
			</Card>
		{/each}
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
		<!-- Recent Activity Timeline -->
		<Card class="bg-white border-stone-200 shadow-xs lg:col-span-2">
			<CardHeader class="border-b border-stone-100 pb-4">
				<CardTitle class="text-lg font-bold text-stone-900 font-sans">Recent Activity</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Track your recent copilot operations</CardDescription>
			</CardHeader>
			<CardContent class="p-6">
				<div class="space-y-6">
					{#each activities as act}
						<div class="flex items-start gap-4">
							<div class="mt-1 shrink-0 p-1.5 rounded-full bg-stone-100 text-stone-500">
								{#if act.type === 'Share2'}
									<Share2 class="size-4 shrink-0" />
								{:else if act.type === 'Languages'}
									<Languages class="size-4 shrink-0" />
								{:else}
									<History class="size-4 shrink-0" />
								{/if}
							</div>
							<div class="flex-1 space-y-1 min-w-0">
								<p class="text-sm font-medium text-stone-800 font-sans truncate">{act.text}</p>
								<p class="text-xs text-stone-400 font-sans">{act.time}</p>
							</div>
						</div>
					{/each}
				</div>
			</CardContent>
		</Card>

		<!-- Quick Actions list -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100 pb-4">
				<CardTitle class="text-lg font-bold text-stone-900 font-sans">Quick Actions</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Jump straight to key features</CardDescription>
			</CardHeader>
			<CardContent class="p-6">
				<div class="space-y-4">
					{#each quickActions as action}
						<a
							href={action.path}
							class="flex items-center gap-3 rounded-lg border border-stone-200 p-3 text-left transition-all hover:bg-stone-50 hover:border-stone-300 outline-none select-none group"
						>
							<div class="p-2 rounded-md bg-stone-100 text-stone-600 group-hover:bg-[#A16207]/10 group-hover:text-[#A16207] transition-colors">
								<action.icon class="size-4 shrink-0" />
							</div>
							<div class="flex-1 min-w-0">
								<p class="text-sm font-semibold text-stone-800 font-sans truncate">{action.name}</p>
								<p class="text-xs text-stone-400 font-sans truncate">{action.desc}</p>
							</div>
						</a>
					{/each}
				</div>
			</CardContent>
		</Card>
	</div>
</div>
