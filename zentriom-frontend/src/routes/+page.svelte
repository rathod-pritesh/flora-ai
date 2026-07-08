<script>
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { appState } from "$lib/states/app.svelte.js";
	import { Sparkles, Languages, Share2, Code, Wrench, Briefcase, ChevronRight, Plus, Trash, X } from "lucide-svelte";

	let activeSection = $state("");
	let showOnboardingModal = $state(false);

	// Onboarding form state
	let fullName = $state("");
	let email = $state("");
	let title = $state("");
	let skillInput = $state("");
	let skillsList = $state([]);
	let locationPref = $state("");
	let availability = $state("Remote");
	let jobType = $state("Full-time");

	let errors = $state({
		name: "",
		email: "",
		title: "",
		skills: "",
		location: ""
	});

	function handleLaunch(e) {
		if (e) e.preventDefault();
		if (appState.user && appState.user.name) {
			goto("/dashboard");
		} else {
			showOnboardingModal = true;
		}
	}

	function addSkill() {
		const trimmed = skillInput.trim();
		if (trimmed && !skillsList.includes(trimmed)) {
			skillsList = [...skillsList, trimmed];
			skillInput = "";
			errors.skills = "";
		}
	}

	function removeSkill(skill) {
		skillsList = skillsList.filter(s => s !== skill);
	}

	function validateAndSubmit(e) {
		if (e) e.preventDefault();
		
		// Reset errors
		errors = { name: "", email: "", title: "", skills: "", location: "" };
		let isValid = true;

		if (!fullName.trim()) {
			errors.name = "Full Name is required";
			isValid = false;
		}

		if (!email.trim()) {
			errors.email = "Email Address is required";
			isValid = false;
		} else if (!email.includes("@") || !email.includes(".")) {
			errors.email = "Please enter a valid email address";
			isValid = false;
		}

		if (!title.trim()) {
			errors.title = "Professional Title is required";
			isValid = false;
		}

		if (skillsList.length < 2) {
			errors.skills = "Please add at least 2 skills (mandatory)";
			isValid = false;
		}

		if (!locationPref.trim()) {
			errors.location = "Location preference is required";
			isValid = false;
		}

		if (isValid) {
			appState.user = {
				name: fullName.trim(),
				email: email.trim(),
				title: title.trim(),
				skills: [...skillsList],
				preferences: {
					location: locationPref.trim(),
					remote: availability,
					jobType: jobType
				}
			};

			if (typeof window !== 'undefined') {
				localStorage.setItem('zentriom_user', JSON.stringify(appState.user));
			}

			showOnboardingModal = false;
			goto("/dashboard");
		}
	}

	onMount(() => {
		const sections = ["features", "how-it-works", "why-zentriom"];
		
		const handleScroll = () => {
			let current = "";
			const threshold = 180; // height offset to match when sticky header covers it
			
			for (const sectionId of sections) {
				const element = document.getElementById(sectionId);
				if (element) {
					const rect = element.getBoundingClientRect();
					// If the section is currently occupying the focal area of the viewport
					if (rect.top <= threshold && rect.bottom > threshold) {
						current = sectionId;
						break;
					}
				}
			}
			activeSection = current;
		};

		window.addEventListener("scroll", handleScroll);
		handleScroll();

		return () => {
			window.removeEventListener("scroll", handleScroll);
		};
	});

	$effect(() => {
		if (typeof window !== 'undefined') {
			if (activeSection) {
				const hash = `#${activeSection}`;
				if (window.location.hash !== hash) {
					history.replaceState(null, "", hash);
				}
			} else {
				if (window.location.hash) {
					history.replaceState(null, "", window.location.pathname);
				}
			}
		}
	});

	const features = [
		{ name: "AI Workspace", desc: "An intelligent canvas to brainstorm, write summaries, and draft documents.", icon: Sparkles },
		{ name: "Grammar Assistant", desc: "Polishes tone, improves readability, and fixes syntax dynamically.", icon: Languages },
		{ name: "LinkedIn Generator", desc: "Creates engaging professional posts tailored by tone and context.", icon: Share2 },
		{ name: "Code Explanation", desc: "Monospace code block breakdown with detailed step-by-step logic.", icon: Code },
		{ name: "Bug Fix Assistant", desc: "Diagnoses runtime errors and stacktraces to propose verified patches.", icon: Wrench },
		{ name: "Job Discovery", desc: "Discovers target careers and calculates skill compatibility metrics.", icon: Briefcase }
	];

	const steps = [
		{ step: "01", title: "Enter your request", desc: "Type in your code snippet, text draft, or job preferences." },
		{ step: "02", title: "LangGraph routing", desc: "Zentriom routes the task to specialized agentic workspaces." },
		{ step: "03", title: "IBM Granite processing", desc: "Advanced language model solves the requested workflow." },
		{ step: "04", title: "Structured outputs", desc: "Receive clean code blocks, grammatical fixes, or job feeds." }
	];

	const benefits = [
		{ title: "No Context Switching", desc: "Keep development, writing, and career building in one dashboard." },
		{ title: "Peak Productivity", desc: "Automate repetitive text drafts and complex code explanations in seconds." },
		{ title: "Developer First", desc: "Monospace interfaces designed to paste code chunks directly." },
		{ title: "Career Growth", desc: "Analyze real job compatibility and cover letter grammar inline." }
	];
</script>

<div class="min-h-screen bg-[#F8F7F4] text-[#1C1917] font-sans selection:bg-[#A16207]/20 selection:text-[#A16207]">
	<!-- Navbar -->
	<header class="sticky top-0 z-50 bg-[#F8F7F4]/80 backdrop-blur-md border-b border-[#E7E5E4] px-4 sm:px-6 lg:px-8">
		<div class="max-w-7xl mx-auto flex h-16 items-center justify-between">
			<div class="flex items-center gap-3">
				<img src="/zentriom_logo_for_dark_theme.png" class="size-11 object-contain" alt="Zentriom" />
				<span class="text-xl font-bold tracking-tight text-[#1C1917] font-sans">Zentriom</span>
			</div>
			<nav class="hidden md:flex items-center gap-6 text-sm font-medium">
				<a 
					href="#features" 
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'features' ? 'text-[#A16207] border-b-2 border-[#A16207]' : 'border-b-2 border-transparent text-stone-500'}"
				>Features</a>
				<a 
					href="#how-it-works" 
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'how-it-works' ? 'text-[#A16207] border-b-2 border-[#A16207]' : 'border-b-2 border-transparent text-stone-500'}"
				>How It Works</a>
				<a 
					href="#why-zentriom" 
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'why-zentriom' ? 'text-[#A16207] border-b-2 border-[#A16207]' : 'border-b-2 border-transparent text-stone-500'}"
				>Why Zentriom</a>
			</nav>
			<button
				onclick={handleLaunch}
				class="inline-flex h-9 items-center justify-center rounded-md bg-[#A16207] px-4 text-xs font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-colors shadow-xs cursor-pointer select-none outline-none"
			>
				Launch Workspace
			</button>
		</div>
	</header>

	<!-- Hero Section -->
	<section class="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
		<div class="max-w-4xl mx-auto text-center space-y-6 relative z-10">
			<div class="inline-flex items-center gap-1.5 rounded-full border border-[#E7E5E4] bg-[#FDFCFB] px-3 py-1 text-xs font-medium text-stone-500 shadow-2xs">
				<span class="size-2 rounded-full bg-[#C2410C] animate-pulse"></span>
				Powered by IBM Granite & LangGraph
			</div>
			<h1 class="text-4xl font-extrabold tracking-tight text-[#1C1917] sm:text-5xl lg:text-6xl font-sans">
				Zentriom – AI Productivity &amp; Career Copilot
			</h1>
			<p class="max-w-2xl mx-auto text-stone-500 text-base sm:text-lg leading-relaxed font-sans">
				An intelligent workspace powered by IBM Granite and LangGraph that helps students, developers, and professionals write better, understand code, fix bugs, create content, and discover career opportunities.
			</p>
			<div class="flex flex-wrap items-center justify-center gap-4 pt-4">
				<button
					onclick={handleLaunch}
					class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
				>
					Get Started
					<ChevronRight class="size-4 ml-1.5" />
				</button>
				<a
					href="#features"
					class="inline-flex h-11 items-center justify-center rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] px-6 text-sm font-semibold text-stone-600 hover:bg-[#F8F7F4] transition-all shadow-2xs"
				>
					Explore Features
				</a>
			</div>
		</div>
	</section>

	<!-- Features Grid -->
	<section id="features" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-[#E7E5E4] bg-[#FDFCFB]/50">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-[#1C1917] sm:text-3xl">Comprehensive Toolkit</h2>
				<p class="text-stone-400 text-xs sm:text-sm">Zentriom routes work automatically across specialized modules to boost outputs.</p>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each features as feat}
					<div class="group border border-[#E7E5E4] bg-[#FDFCFB] rounded-xl p-6 shadow-2xs hover:border-[#A16207]/30 transition-all">
						<div class="p-2.5 rounded-lg bg-stone-100 text-stone-600 group-hover:bg-[#A16207]/10 group-hover:text-[#A16207] transition-all w-fit mb-4">
							<feat.icon class="size-5 shrink-0" />
						</div>
						<h3 class="text-base font-bold text-stone-900 mb-2">{feat.name}</h3>
						<p class="text-stone-400 text-xs leading-relaxed font-sans">{feat.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- How It Works Section -->
	<section id="how-it-works" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-[#E7E5E4]">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-[#1C1917] sm:text-3xl">How It Works</h2>
				<p class="text-stone-400 text-xs sm:text-sm">Seamless workflow routing designed for single-user workspaces.</p>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each steps as step}
					<div class="relative border border-[#E7E5E4] bg-[#FDFCFB] rounded-xl p-6 shadow-2xs">
						<span class="text-3xl font-extrabold text-[#C2410C]/20 block mb-2">{step.step}</span>
						<h3 class="text-sm font-bold text-stone-900 mb-1">{step.title}</h3>
						<p class="text-stone-400 text-xs leading-relaxed font-sans">{step.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Why Zentriom Section -->
	<section id="why-zentriom" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-[#E7E5E4] bg-[#FDFCFB]/50">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-[#1C1917] sm:text-3xl">Why Zentriom</h2>
				<p class="text-stone-400 text-xs sm:text-sm">Designed specifically to enhance your personal flow.</p>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
				{#each benefits as ben}
					<div class="border border-[#E7E5E4] bg-[#FDFCFB] rounded-xl p-6 shadow-2xs">
						<h3 class="text-sm font-bold text-stone-900 mb-1.5">{ben.title}</h3>
						<p class="text-stone-400 text-xs leading-relaxed font-sans">{ben.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- CTA Section -->
	<section class="py-20 px-4 sm:px-6 lg:px-8 border-t border-[#E7E5E4]">
		<div class="max-w-4xl mx-auto rounded-2xl border border-[#E7E5E4] bg-[#FDFCFB] p-8 md:p-12 text-center shadow-xs space-y-6">
			<h2 class="text-3xl font-extrabold tracking-tight text-[#1C1917] sm:text-4xl">
				Ready to start using Zentriom?
			</h2>
			<p class="max-w-md mx-auto text-stone-500 text-xs sm:text-sm leading-relaxed">
				Launch the copilot canvas and access grammar fixer, code explainer, LinkedIn template engines, and jobs dashboard instantly.
			</p>
			<div>
				<button
					onclick={handleLaunch}
					class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
				>
					Launch Workspace
					<ChevronRight class="size-4 ml-1.5" />
				</button>
			</div>
		</div>
	</section>

	<!-- Footer -->
	<footer class="border-t border-[#E7E5E4] py-8 px-4 sm:px-6 lg:px-8 text-center text-stone-400 text-[11px]">
		<p>© {new Date().getFullYear()} Zentriom AI. Built with IBM Granite &amp; LangGraph. All rights reserved.</p>
	</footer>

	<!-- Onboarding Modal Overlay -->
	{#if showOnboardingModal}
		<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2D2926]/60 backdrop-blur-xs transition-opacity duration-300">
			<!-- Modal Content -->
			<div class="bg-[#FDFCFB] border border-[#E7E5E4] rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-6 md:p-8 space-y-6 shadow-2xl relative">
				
				<!-- Close Button -->
				<button 
					onclick={() => showOnboardingModal = false} 
					class="absolute top-4 right-4 text-stone-400 hover:text-stone-600 outline-none select-none transition-colors cursor-pointer"
					aria-label="Close modal"
				>
					<X class="size-5" />
				</button>

				<!-- Header -->
				<div class="space-y-1">
					<h3 class="text-xl font-bold tracking-tight text-[#1C1917] font-sans">Configure Your Onboarding Profile</h3>
					<p class="text-[#A16207] text-[11px] font-sans font-semibold">Step inside your developer dashboard using custom parameters</p>
				</div>

				<form onsubmit={validateAndSubmit} class="space-y-4">
					<!-- Full Name -->
					<div class="space-y-1">
						<label for="onboarding-fullname" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Full Name *</label>
						<input 
							id="onboarding-fullname"
							type="text" 
							bind:value={fullName} 
							placeholder="e.g. Pritesh Rathod" 
							class="w-full h-10 px-3 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs" 
						/>
						{#if errors.name}
							<p class="text-red-600 text-[10px] font-semibold mt-0.5">{errors.name}</p>
						{/if}
					</div>

					<!-- Email Address -->
					<div class="space-y-1">
						<label for="onboarding-email" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Email Address *</label>
						<input 
							id="onboarding-email"
							type="email" 
							bind:value={email} 
							placeholder="e.g. pritesh@example.com" 
							class="w-full h-10 px-3 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs" 
						/>
						{#if errors.email}
							<p class="text-red-600 text-[10px] font-semibold mt-0.5">{errors.email}</p>
						{/if}
					</div>

					<!-- Professional Title -->
					<div class="space-y-1">
						<label for="onboarding-title" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Professional Title *</label>
						<input 
							id="onboarding-title"
							type="text" 
							bind:value={title} 
							placeholder="e.g. Lead Developer / Student" 
							class="w-full h-10 px-3 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs" 
						/>
						{#if errors.title}
							<p class="text-red-600 text-[10px] font-semibold mt-0.5">{errors.title}</p>
						{/if}
					</div>

					<!-- Skills Matrix -->
					<div class="space-y-1">
						<label for="onboarding-skills" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Skills Matrix (Add 2-3 mandatory) *</label>
						<div class="flex gap-2">
							<input 
								id="onboarding-skills"
								type="text" 
								bind:value={skillInput} 
								onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSkill(); } }}
								placeholder="Type skill & press Enter or click +" 
								class="flex-1 h-10 px-3 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs" 
							/>
							<button 
								type="button" 
								onclick={addSkill} 
								class="h-10 w-10 flex items-center justify-center rounded-lg bg-[#A16207]/10 hover:bg-[#A16207]/20 text-[#A16207] transition-colors outline-none cursor-pointer"
							>
								<Plus class="size-4" />
							</button>
						</div>
						{#if errors.skills}
							<p class="text-red-600 text-[10px] font-semibold mt-0.5">{errors.skills}</p>
						{/if}
						
						<!-- Added skills list -->
						{#if skillsList.length > 0}
							<div class="flex flex-wrap gap-1.5 mt-2">
								{#each skillsList as skill}
									<span class="inline-flex items-center gap-1.5 bg-[#A16207]/10 text-[#A16207] text-[10px] font-semibold px-2 py-0.5 rounded-md">
										{skill}
										<button 
											type="button" 
											onclick={() => removeSkill(skill)} 
											class="text-[#A16207] hover:text-red-600 font-bold outline-none cursor-pointer"
										>
											×
										</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>

					<!-- Location, Availability, Job Type -->
					<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
						<!-- Location -->
						<div class="space-y-1">
							<label for="onboarding-location" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Location *</label>
							<input 
								id="onboarding-location"
								type="text" 
								bind:value={locationPref} 
								placeholder="e.g. London" 
								class="w-full h-10 px-3 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] transition-all font-sans text-xs" 
							/>
							{#if errors.location}
								<p class="text-red-600 text-[10px] font-semibold mt-0.5">{errors.location}</p>
							{/if}
						</div>

						<!-- Availability -->
						<div class="space-y-1">
							<label for="onboarding-availability" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Availability *</label>
							<select 
								id="onboarding-availability"
								bind:value={availability} 
								class="w-full h-10 px-2 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 focus:outline-hidden focus:border-[#A16207] transition-all font-sans text-xs"
							>
								<option value="Remote">Remote</option>
								<option value="Onsite">Onsite</option>
								<option value="Hybrid">Hybrid</option>
							</select>
						</div>

						<!-- Job Type -->
						<div class="space-y-1">
							<label for="onboarding-jobtype" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Job Type *</label>
							<select 
								id="onboarding-jobtype"
								bind:value={jobType} 
								class="w-full h-10 px-2 rounded-lg border border-[#E7E5E4] bg-[#FDFCFB] text-stone-900 focus:outline-hidden focus:border-[#A16207] transition-all font-sans text-xs"
							>
								<option value="Full-time">Full-time</option>
								<option value="Part-time">Part-time</option>
								<option value="Contract">Contract</option>
								<option value="Internship">Internship</option>
							</select>
						</div>
					</div>

					<!-- Form Actions -->
					<div class="flex items-center justify-end gap-3 pt-4 border-t border-[#E7E5E4]">
						<button 
							type="button" 
							onclick={() => showOnboardingModal = false} 
							class="px-4 py-2 border border-[#E7E5E4] text-stone-600 rounded-lg hover:bg-stone-50 transition-colors text-xs font-semibold cursor-pointer outline-none"
						>
							Cancel
						</button>
						<button 
							type="submit" 
							class="px-5 py-2 bg-[#A16207] text-[#F8F7F4] rounded-lg hover:bg-[#A16207]/90 transition-colors text-xs font-semibold cursor-pointer outline-none shadow-sm"
						>
							Launch Workspace
						</button>
					</div>
				</form>
			</div>
		</div>
	{/if}
</div>
