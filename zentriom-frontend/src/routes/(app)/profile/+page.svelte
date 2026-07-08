<script>
	import { appState } from "$lib/states/app.svelte.js";
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Badge } from "$lib/components/ui/badge/index.js";
	import { Avatar, AvatarFallback } from "$lib/components/ui/avatar/index.js";
	import { User, Settings, Plus, Trash, Check } from "lucide-svelte";

	let name = $state(appState.user?.name || "Pritesh Rathod");
	let email = $state(appState.user?.email || "pritesh.rathod@example.com");
	let title = $state(appState.user?.title || "Senior Frontend Architect");
	let newSkill = $state("");
	let skills = $state(appState.user?.skills && appState.user.skills.length > 0 ? appState.user.skills : ["Svelte 5", "TypeScript", "Tailwind CSS v4", "System Architecture", "Vite"]);
	let preferences = $state({
		location: appState.user?.preferences?.location || "San Francisco, CA",
		remote: appState.user?.preferences?.remote || "Hybrid",
		jobType: appState.user?.preferences?.jobType || "Full-time"
	});

	let saveStatus = $state(false);

	function addSkill() {
		if (newSkill.trim() && !skills.includes(newSkill.trim())) {
			skills = [...skills, newSkill.trim()];
			newSkill = "";
		}
	}

	function removeSkill(skill) {
		skills = skills.filter(s => s !== skill);
	}

	function handleSave() {
		appState.user = {
			name: name.trim(),
			email: email.trim(),
			title: title.trim(),
			skills: [...skills],
			preferences: {
				location: preferences.location.trim(),
				remote: preferences.remote,
				jobType: preferences.jobType
			}
		};
		if (typeof window !== 'undefined') {
			localStorage.setItem('zentriom_user', JSON.stringify(appState.user));
		}
		saveStatus = true;
		setTimeout(() => saveStatus = false, 1500);
	}
</script>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
	<!-- Left Side: Profile Summary Card -->
	<div class="lg:col-span-1 space-y-6">
		<Card class="bg-white border-stone-200 shadow-xs text-center">
			<CardContent class="p-6 flex flex-col items-center">
				<Avatar class="size-20 border border-stone-200 shadow-xs mb-4">
					<AvatarFallback class="bg-[#A16207] text-white text-2xl font-bold font-sans">
						{name ? name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : 'PR'}
					</AvatarFallback>
				</Avatar>
				<h3 class="text-base font-bold text-stone-900 font-sans">{name}</h3>
				<p class="text-xs text-stone-400 font-sans mt-0.5">{title}</p>
				<div class="mt-4 flex flex-wrap gap-1.5 justify-center">
					<Badge variant="outline" class="bg-stone-50 border-stone-200 text-stone-600 text-[9px] font-sans">Active Profile</Badge>
					<Badge variant="outline" class="bg-emerald-50 text-emerald-800 border-emerald-100 text-[9px] font-sans">Copilot Level 3</Badge>
				</div>
			</CardContent>
		</Card>
	</div>

	<!-- Right Side: Details forms -->
	<div class="lg:col-span-2 space-y-6">
		<!-- Personal Details Card -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100">
				<CardTitle class="text-base font-bold text-stone-900 font-sans">User Profile Details</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Update primary contact and designation information</CardDescription>
			</CardHeader>
			<CardContent class="p-6 space-y-4">
				<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
					<div class="space-y-1">
						<label for="name" class="text-xs font-semibold text-stone-700 font-sans">Full Name</label>
						<Input id="name" bind:value={name} class="h-9 bg-white border-stone-200 text-xs font-sans" />
					</div>
					<div class="space-y-1">
						<label for="email" class="text-xs font-semibold text-stone-700 font-sans">Email Address</label>
						<Input id="email" bind:value={email} class="h-9 bg-white border-stone-200 text-xs font-sans" />
					</div>
				</div>
				<div class="space-y-1">
					<label for="title" class="text-xs font-semibold text-stone-700 font-sans">Professional Title</label>
					<Input id="title" bind:value={title} class="h-9 bg-white border-stone-200 text-xs font-sans" />
				</div>
			</CardContent>
		</Card>

		<!-- Skills Matrix Card -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100">
				<CardTitle class="text-base font-bold text-stone-900 font-sans">Skills Matrix</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Skills matching will calculate Job Match scores automatically</CardDescription>
			</CardHeader>
			<CardContent class="p-6 space-y-4">
				<!-- Skill tags list -->
				<div class="flex flex-wrap gap-1.5 min-h-[36px]">
					{#each skills as skill}
						<Badge variant="secondary" class="bg-stone-50 border border-stone-200 text-stone-600 text-[10px] font-sans flex items-center gap-1.5">
							{skill}
							<button onclick={() => removeSkill(skill)} class="text-stone-400 hover:text-red-500 font-bold text-[9px] outline-none">×</button>
						</Badge>
					{/each}
				</div>

				<!-- Skill input Form -->
				<div class="flex gap-2">
					<Input
						bind:value={newSkill}
						onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSkill(); } }}
						placeholder="Add new skill..."
						class="h-9 bg-white border-stone-200 text-xs font-sans"
					/>
					<Button onclick={addSkill} class="bg-[#A16207]/10 hover:bg-[#A16207]/20 text-[#A16207] size-9 p-0 shrink-0 outline-none">
						<Plus class="size-4" />
					</Button>
				</div>
			</CardContent>
		</Card>

		<!-- Career Preferences Card -->
		<Card class="bg-white border-stone-200 shadow-xs">
			<CardHeader class="border-b border-stone-100">
				<CardTitle class="text-base font-bold text-stone-900 font-sans">Career Preferences</CardTitle>
				<CardDescription class="text-xs text-stone-400 font-sans">Job Discovery matches location and remote configurations</CardDescription>
			</CardHeader>
			<CardContent class="p-6 space-y-4">
				<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
					<div class="space-y-1">
						<label for="location" class="text-xs font-semibold text-stone-700 font-sans">Location</label>
						<Input id="location" bind:value={preferences.location} class="h-9 bg-white border-stone-200 text-xs font-sans" />
					</div>
					<div class="space-y-1">
						<label for="remote" class="text-xs font-semibold text-stone-700 font-sans">Availability</label>
						<Input id="remote" bind:value={preferences.remote} class="h-9 bg-white border-stone-200 text-xs font-sans" />
					</div>
					<div class="space-y-1">
						<label for="jobType" class="text-xs font-semibold text-stone-700 font-sans">Job Type</label>
						<Input id="jobType" bind:value={preferences.jobType} class="h-9 bg-white border-stone-200 text-xs font-sans" />
					</div>
				</div>
				<div class="flex justify-end pt-2">
					<Button onclick={handleSave} class="bg-[#A16207] text-white hover:bg-[#A16207]/90 h-9 px-5 text-xs font-sans">
						{#if saveStatus}
							<Check class="size-4 mr-2" /> Saved Successfully
						{:else}
							Save Changes
						{/if}
					</Button>
				</div>
			</CardContent>
		</Card>
	</div>
</div>
