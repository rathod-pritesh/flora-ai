<script>
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { authStore } from "$lib/stores/auth.svelte.js";
	import { Sparkles, Languages, Share2, Code, Wrench, Briefcase, ChevronRight, User, LogOut, Settings } from "lucide-svelte";
	import { Avatar, AvatarFallback } from "$lib/components/ui/avatar/index.js";
	import { replaceState } from '$app/navigation';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem,
		DropdownMenuLabel,
		DropdownMenuSeparator,
		DropdownMenuGroup
	} from "$lib/components/ui/dropdown-menu/index.js";
	import LoginForm from "$lib/components/auth/LoginForm.svelte";
	import SignUpForm from "$lib/components/auth/SignUpForm.svelte";
	import { loginWithGoogle } from '$lib/services/auth.js';

import {
	setAuth
} from '$lib/stores/auth.svelte.js';

	let activeSection = $state("");
	let authTab = $state("login"); // "login" | "signup"

	// Scroll helper to Auth card
	function scrollToAuth() {
		const authEl = document.getElementById("auth-section");
		if (authEl) {
			authEl.scrollIntoView({ behavior: "smooth" });
		}
	}

	async function handleGoogleLogin() {
	try {
		console.log(import.meta.env.VITE_GOOGLE_CLIENT_ID);
		window.google.accounts.id.initialize({
			client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,

			callback: async (response) => {
				try {
					const result = await loginWithGoogle(
						response.credential
					);

					setAuth(
						result.user,
						result.token
					);

					goto('/dashboard');
				}
				catch (err) {
					console.error(err);
					alert('Google login failed');
				}
			}
		});

		window.google.accounts.id.prompt();
	}
	catch (err) {
		console.error(err);
		alert('Unable to start Google login');
	}
}

	function handleLogOut() {
		authStore.user = null;
		authStore.token = null;
		authStore.isAuthenticated = false;
		authStore.loading = false;
	}

	// Watch URL parameters to trigger auto-scroll to authentication section if redirected
	$effect(() => {
		if ($page.url.searchParams.get("showAuth") === "true") {
			scrollToAuth();
		}
	});

	onMount(() => {
		const sections = ["features", "how-it-works", "why-zentriom"];
		
		const handleScroll = () => {
			let current = "";
			const threshold = 180;
			
			for (const sectionId of sections) {
				const element = document.getElementById(sectionId);
				if (element) {
					const rect = element.getBoundingClientRect();
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
				<span class="text-xl font-bold tracking-tight text-[#1C1917] font-sans">
					<a href="/">Zentriom</a>
				</span>
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

			{#if authStore.isAuthenticated}
				<div class="flex items-center gap-4">
					<a
						href="/dashboard"
						class="inline-flex h-9 items-center justify-center rounded-md bg-[#A16207] px-4 text-xs font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-colors shadow-xs cursor-pointer select-none outline-none"
					>
						Dashboard
					</a>
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
								<DropdownMenuItem onclick={() => goto("/settings")} class="flex items-center gap-2 px-2 py-1.5 text-sm text-stone-700 hover:bg-stone-50 hover:text-stone-900 rounded-sm cursor-pointer outline-none font-sans">
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
			{:else}
				<div class="flex items-center gap-3">
					<button
						onclick={scrollToAuth}
						class="inline-flex h-9 items-center justify-center rounded-md border border-stone-200 bg-white px-4 text-xs font-semibold text-stone-700 hover:bg-stone-50 transition-colors cursor-pointer select-none outline-none"
					>
						Login
					</button>
					<button
						onclick={scrollToAuth}
						class="inline-flex h-9 items-center justify-center rounded-md bg-[#A16207] px-4 text-xs font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-colors shadow-xs cursor-pointer select-none outline-none"
					>
						Get Started
					</button>
				</div>
			{/if}
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
				{#if authStore.isAuthenticated}
					<a
						href="/dashboard"
						class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
					>
						Dashboard
						<ChevronRight class="size-4 ml-1.5" />
					</a>
				{:else}
					<button
						onclick={scrollToAuth}
						class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-[#F8F7F4] hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
					>
						Get Started
						<ChevronRight class="size-4 ml-1.5" />
					</button>
				{/if}
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

	<!-- Authentication Section -->
	{#if !authStore.isAuthenticated}
		<section id="auth-section" class="py-16 px-4 sm:px-6 lg:px-8 border-t border-[#E7E5E4] bg-[#FDFCFB]/30">
			<div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
				<div class="space-y-6">
					<h2 class="text-3xl font-extrabold tracking-tight text-[#1C1917] sm:text-4xl font-sans leading-tight">
						Experience the power of Granite AI
					</h2>
					<p class="text-stone-500 font-sans text-sm sm:text-base leading-relaxed">
						Join developers and professionals who use Zentriom to automate their writing, analyze code, fix bugs, and track job matches in one unified environment.
					</p>
					<ul class="space-y-3">
						<li class="flex items-center gap-3 text-xs font-semibold text-stone-600">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							IBM Granite & LangGraph under the hood
						</li>
						<li class="flex items-center gap-3 text-xs font-semibold text-stone-600">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							Active code explainers and grammar fixer tools
						</li>
						<li class="flex items-center gap-3 text-xs font-semibold text-stone-600">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							Zero-friction signup, get access instantly
						</li>
					</ul>
				</div>

				<div class="w-full max-w-md mx-auto rounded-2xl border border-[#E7E5E4] bg-white p-6 sm:p-8 shadow-sm space-y-6">
					<!-- Tab Headers -->
					<div class="flex border-b border-[#E7E5E4]">
						<button
							onclick={() => authTab = "login"}
							class="flex-1 pb-3 text-sm font-bold text-center transition-all cursor-pointer outline-none select-none
								{authTab === 'login' ? 'text-[#A16207] border-b-2 border-[#A16207]' : 'text-stone-400 border-b-2 border-transparent hover:text-stone-600'}"
						>
							Sign In
						</button>
						<button
							onclick={() => authTab = "signup"}
							class="flex-1 pb-3 text-sm font-bold text-center transition-all cursor-pointer outline-none select-none
								{authTab === 'signup' ? 'text-[#A16207] border-b-2 border-[#A16207]' : 'text-stone-400 border-b-2 border-transparent hover:text-stone-600'}"
						>
							Create Account
						</button>
					</div>

					<!-- Continue with Google button -->
					<div class="space-y-4">
						<button
							type="button"
							onclick={handleGoogleLogin}
							class="w-full h-10 border border-[#E7E5E4] rounded-lg bg-white text-stone-700 hover:bg-stone-50 transition-colors text-xs font-bold flex items-center justify-center gap-2 outline-none cursor-pointer"
						>
							<!-- Google Color Logo Icon -->
							<svg class="size-4 shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
								<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
								<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
								<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
							</svg>
							<span>Continue with Google</span>
						</button>

						<div class="relative flex py-1 items-center">
							<div class="flex-grow border-t border-stone-200"></div>
							<span class="flex-shrink mx-4 text-[9px] font-bold text-stone-400 uppercase tracking-wider">OR CONTINUE WITH EMAIL</span>
							<div class="flex-grow border-t border-stone-200"></div>
						</div>
					</div>

					<!-- Form components -->
					{#if authTab === "login"}
						<LoginForm />
					{:else}
						<SignUpForm />
					{/if}
				</div>
			</div>
		</section>
	{/if}

	<!-- Footer -->
	<footer class="border-t border-[#E7E5E4] py-8 px-4 sm:px-6 lg:px-8 text-center text-stone-400 text-[11px]">
		<p>© {new Date().getFullYear()} Zentriom AI. Built with IBM Granite &amp; LangGraph. All rights reserved.</p>
	</footer>
</div>
