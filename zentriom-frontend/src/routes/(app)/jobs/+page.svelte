<script>
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Briefcase, Search, Sparkles } from 'lucide-svelte';

	let searchQuery = $state('');
	let locationQuery = $state('');
	let isSearching = $state(false);

	let jobs = $state([
		{
			id: 1,
			title: 'Senior AI Frontend Engineer',
			company: 'Zentriom AI',
			location: 'San Francisco, CA (Hybrid)',
			score: 95,
			matchedSkills: ['Svelte 5', 'Tailwind CSS', 'Vite', 'TypeScript'],
			missingSkills: ['GraphQL']
		},
		{
			id: 2,
			title: 'Full Stack Developer',
			company: 'Granite Tech',
			location: 'Remote',
			score: 82,
			matchedSkills: ['SvelteKit', 'Vite', 'NodeJS'],
			missingSkills: ['Docker', 'LangGraph']
		},
		{
			id: 3,
			title: 'Product Engineer (AI Copilots)',
			company: 'Apex Solutions',
			location: 'New York, NY (Hybrid)',
			score: 68,
			matchedSkills: ['Tailwind CSS', 'JavaScript'],
			missingSkills: ['Python', 'PyTorch', 'Zod']
		}
	]);

	const filteredJobs = $derived(
		jobs.filter(
			(j) =>
				(j.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
					j.company.toLowerCase().includes(searchQuery.toLowerCase())) &&
				j.location.toLowerCase().includes(locationQuery.toLowerCase())
		)
	);

	function handleSearch() {
		isSearching = true;
		setTimeout(() => (isSearching = false), 500);
	}
</script>

<div class="space-y-6">
	<!-- Search Filters Header Card -->
	<Card class="bg-white border-stone-200 shadow-xs">
		<CardContent class="p-4 flex flex-col md:flex-row gap-3">
			<div class="flex-1 flex gap-2">
				<div class="relative flex-1">
					<Search class="absolute left-3 top-3 size-4 text-stone-400 shrink-0" />
					<Input
						bind:value={searchQuery}
						placeholder="Search job title or company..."
						class="pl-9 bg-white border-stone-200 text-xs font-sans h-10"
					/>
				</div>
				<Input
					bind:value={locationQuery}
					placeholder="Location..."
					class="w-40 bg-white border-stone-200 text-xs font-sans h-10"
				/>
			</div>
			<Button
				onclick={handleSearch}
				disabled={isSearching}
				class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-10 px-5 text-xs font-sans"
			>
				{isSearching ? 'Searching...' : 'Find Jobs'}
			</Button>
		</CardContent>
	</Card>

	<!-- Job Cards Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		{#each filteredJobs as job}
			<Card class="bg-white border-stone-200 shadow-xs hover:border-stone-300 transition-all">
				<CardHeader
					class="border-b border-stone-100 flex flex-row justify-between items-start pb-4"
				>
					<div class="space-y-1">
						<CardTitle class="text-base font-bold text-stone-900 font-sans">{job.title}</CardTitle>
						<p class="text-xs font-semibold text-stone-500 font-sans">
							{job.company} • {job.location}
						</p>
					</div>
					<div class="text-right">
						<span
							class="text-[10px] font-bold uppercase tracking-wider text-stone-400 block font-sans"
							>Match Score</span
						>
						<span
							class="text-lg font-extrabold font-sans {job.score >= 90
								? 'text-[#A16207]'
								: job.score >= 80
									? 'text-[#C2410C]'
									: 'text-stone-500'}"
						>
							{job.score}%
						</span>
					</div>
				</CardHeader>
				<CardContent class="p-6 space-y-4">
					<!-- Progress Bar UI -->
					<div class="w-full bg-stone-100 h-2 rounded-full overflow-hidden">
						<div
							class="h-full rounded-full transition-all duration-500 {job.score >= 90
								? 'bg-[#A16207]'
								: job.score >= 80
									? 'bg-[#C2410C]'
									: 'bg-stone-400'}"
							style="width: {job.score}%"
						></div>
					</div>

					<!-- Skill Gap UI -->
					<div class="space-y-2">
						<span
							class="text-[10px] font-bold text-stone-400 uppercase tracking-wider block font-sans"
							>Skill Coverage</span
						>
						<div class="flex flex-wrap gap-1.5">
							{#each job.matchedSkills as skill}
								<Badge
									variant="outline"
									class="bg-emerald-50 text-emerald-800 border-emerald-100 text-[10px] font-sans"
								>
									{skill}
								</Badge>
							{/each}
							{#each job.missingSkills as skill}
								<Badge
									variant="outline"
									class="bg-red-50 text-red-800 border-red-100 text-[10px] font-sans"
								>
									Gap: {skill}
								</Badge>
							{/each}
						</div>
					</div>
				</CardContent>
			</Card>
		{/each}
	</div>
</div>
