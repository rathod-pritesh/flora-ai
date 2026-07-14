<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authStore, loadAuth, logout } from '$lib/stores/auth.svelte.js';
	import {
		Sparkles,
		Languages,
		Share2,
		Code,
		Wrench,
		Briefcase,
		ChevronRight,
		Settings,
		LogOut,
		FileText
	} from 'lucide-svelte';
	import { Avatar, AvatarFallback, AvatarImage } from '$lib/components/ui/avatar/index.js';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem,
		DropdownMenuLabel,
		DropdownMenuSeparator,
		DropdownMenuGroup
	} from '$lib/components/ui/dropdown-menu/index.js';
	import LoginForm from '$lib/components/auth/LoginForm.svelte';
	import SignUpForm from '$lib/components/auth/SignUpForm.svelte';
	import { loginWithGoogle } from '$lib/services/auth.js';
	import { setAuth } from '$lib/stores/auth.svelte.js';
	import { initGoogleLogin } from '$lib/services/google.js';
	import { toast } from 'svelte-sonner';

	let activeSection = $state('');
	let imageFailed = $state(false);
	let authTab = $state('login');

	function scrollToAuth() {
		const authEl = document.getElementById('auth-section');
		if (authEl) {
			authEl.scrollIntoView({ behavior: 'smooth' });
		}
	}

	function showLogin() {
		authTab = 'login';
		scrollToAuth();
	}

	function showSignup() {
		authTab = 'signup';
		scrollToAuth();
	}

	const getInitials = (name) => {
		if (!name) return 'TU';
		const parts = name.trim().split(/\s+/);
		if (parts.length === 0) return 'TU';
		if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
		return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
	};

	onMount(() => {
		loadAuth();
	});

	onMount(() => {
		initGoogleLogin(async (response) => {
			try {
				const result = await loginWithGoogle(response.credential);
				setAuth(result.user, result.token);
				toast.success("Signed in with Google.");
				goto('/dashboard');
			} catch (error) {
				console.error('Google login verification failed:', error);
				if (error.message && error.message.includes('registered with another account')) {
					toast.info("This email is already registered with password login. Please sign in using your password or reset your password if needed.");
				} else {
					toast.error(error.message || "Unable to sign in with Google.");
				}
			}
		}, 'google-signin-button');
	});

	function handleLogOut() {
		logout();
		toast.success('You have been signed out.');
		goto('/');
	}

	$effect(() => {
		if ($page.url.searchParams.get('showAuth') === 'true') {
			showLogin();
			goto('/', { replaceState: true, noScroll: true });
		}
	});

	function navigateToSection(e, sectionId) {
		if (e) e.preventDefault();
		const element = document.getElementById(sectionId);
		if (element) {
			element.scrollIntoView({ behavior: 'smooth' });
			history.pushState(null, '', `#${sectionId}`);
			activeSection = sectionId;
		}
	}

	onMount(() => {
		const sections = ['features', 'how-it-works', 'why-zentriom'];

		const handleScroll = () => {
			let current = '';
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

			// Update URL hash dynamically during scroll without polluting history stack
			if (current) {
				if (window.location.hash !== `#${current}`) {
					history.replaceState(null, '', `#${current}`);
				}
			} else {
				if (window.location.hash && window.location.hash !== '#') {
					history.replaceState(
						null,
						'',
						window.location.pathname + window.location.search
					);
				}
			}
		};

		const handleHashChange = () => {
			const hash = window.location.hash.slice(1);
			if (hash) {
				const element = document.getElementById(hash);
				if (element) {
					element.scrollIntoView({ behavior: 'smooth' });
				}
			}
		};

		window.addEventListener('scroll', handleScroll);
		window.addEventListener('hashchange', handleHashChange);
		handleScroll();

		// Scroll to initial hash if loaded directly
		setTimeout(handleHashChange, 100);

		return () => {
			window.removeEventListener('scroll', handleScroll);
			window.removeEventListener('hashchange', handleHashChange);
		};
	});

	const features = [
		{
			name: 'LinkedIn Generator',
			desc: 'Generate professional LinkedIn posts tailored to your experience and career goals.',
			icon: Share2,
			path: '/linkedin'
		},
		{
			name: 'Grammar Assistant',
			desc: 'Improve grammar, readability, and writing quality with AI-powered assistance.',
			icon: Languages,
			path: '/grammar'
		},
		{
			name: 'Code Explanation',
			desc: 'Understand complex programming logic with interactive, step-by-step explanations.',
			icon: Code,
			path: '/code-explainer'
		},
		{
			name: 'Bug Fix Assistant',
			desc: 'Resolve software bugs and debug runtime errors using intelligent code suggestions.',
			icon: Wrench,
			underDevelopment: true
		},
		{
			name: 'Resume Review',
			desc: 'Analyze resume quality and get personalized feedback to improve your profile.',
			icon: FileText,
			underDevelopment: true
		},
		{
			name: 'Job Match',
			desc: 'Discover relevant career opportunities based on your skills and experience.',
			icon: Briefcase,
			underDevelopment: true
		}
	];

	const steps = [
		{
			step: '01',
			title: 'Enter your request',
			desc: 'Type in your code snippet, text draft, or job preferences.'
		},
		{
			step: '02',
			title: 'LangGraph routing',
			desc: 'Zentriom routes the task to specialized agentic workspaces.'
		},
		{
			step: '03',
			title: 'IBM Granite processing',
			desc: 'Advanced language model solves the requested workflow.'
		},
		{
			step: '04',
			title: 'Structured outputs',
			desc: 'Receive clean code blocks, grammatical fixes, or job feeds.'
		}
	];

	const benefits = [
		{
			title: 'No Context Switching',
			desc: 'Keep development, writing, and career building in one dashboard.'
		},
		{
			title: 'Peak Productivity',
			desc: 'Automate repetitive text drafts and complex code explanations in seconds.'
		},
		{
			title: 'Developer First',
			desc: 'Monospace interfaces designed to paste code chunks directly.'
		},
		{
			title: 'Career Growth',
			desc: 'Analyze real job compatibility and cover letter grammar inline.'
		}
	];
</script>

<svelte:head>
	<title>Zentriom AI Powered Productivity and Career Assistant</title>
	<meta name="description" content="Zentriom AI Powered Productivity and Career Assistant is an intelligent workspace powered by IBM Granite and LangGraph." />
	<meta property="og:title" content="Zentriom AI Powered Productivity and Career Assistant" />
	<meta property="og:description" content="An intelligent workspace powered by IBM Granite and LangGraph that helps students, developers, and professionals write better, understand code, fix bugs, create content, and discover career opportunities." />
</svelte:head>

<div
	class="min-h-screen bg-background text-foreground font-sans selection:bg-[#A16207]/20 selection:text-[#A16207]"
>
	<header
		class="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border px-4 sm:px-6 lg:px-8 text-foreground"
	>
		<div class="max-w-7xl mx-auto flex h-16 items-center justify-between">
			<div class="flex items-center gap-3">
				<img src="/logo.png" class="size-11 object-contain" alt="Zentriom" />
				<span class="text-xl font-bold tracking-tight text-foreground font-sans">
					<a href="/">Zentriom</a>
				</span>
			</div>
			<nav class="hidden md:flex items-center gap-6 text-sm font-medium">
				<a
					href="#features"
					onclick={(e) => navigateToSection(e, 'features')}
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'features'
						? 'text-[#A16207] border-b-2 border-[#A16207]'
						: 'border-b-2 border-transparent text-muted-foreground'}"
				>
					Features
				</a>
				<a
					href="#how-it-works"
					onclick={(e) => navigateToSection(e, 'how-it-works')}
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'how-it-works'
						? 'text-[#A16207] border-b-2 border-[#A16207]'
						: 'border-b-2 border-transparent text-muted-foreground'}"
				>
					How It Works
				</a>
				<a
					href="#why-zentriom"
					onclick={(e) => navigateToSection(e, 'why-zentriom')}
					class="pb-1 hover:text-[#A16207] transition-all {activeSection === 'why-zentriom'
						? 'text-[#A16207] border-b-2 border-[#A16207]'
						: 'border-b-2 border-transparent text-muted-foreground'}"
				>
					Why Zentriom
				</a>
			</nav>

			{#if authStore.isAuthenticated}
				<div class="flex items-center gap-4">
					<a
						href="/dashboard"
						class="inline-flex h-9 items-center justify-center rounded-md bg-[#A16207] px-4 text-xs font-semibold text-primary-foreground hover:bg-[#A16207]/90 transition-colors shadow-xs cursor-pointer select-none outline-none"
					>
						Dashboard
					</a>
					<DropdownMenu>
						<DropdownMenuTrigger
							class="rounded-full outline-none focus-visible:ring-2 focus-visible:ring-[#A16207]/50 select-none"
						>
							<Avatar class="size-9 border border-border cursor-pointer">
								{#if authStore.user?.picture && !imageFailed}
									<AvatarImage
										src={authStore.cachedAvatar || authStore.user.picture}
										alt={authStore.user.name}
										onerror={() => (imageFailed = true)}
									/>
								{/if}
								<AvatarFallback
									class="bg-muted text-muted-foreground hover:bg-accent text-sm font-semibold flex items-center justify-center"
								>
									{getInitials(authStore.user?.name)}
								</AvatarFallback>
							</Avatar>
						</DropdownMenuTrigger>
						<DropdownMenuContent
							align="end"
							class="w-56 bg-card border border-border shadow-lg rounded-md p-1 text-foreground"
						>
							<DropdownMenuLabel
								class="px-2 py-1.5 text-sm font-semibold text-foreground font-sans"
							>
								My Account
							</DropdownMenuLabel>
							<DropdownMenuSeparator class="my-1 border-t border-border" />
							<DropdownMenuGroup>
								<DropdownMenuItem
									onclick={() => goto('/settings')}
									class="flex items-center gap-2 px-2 py-1.5 text-sm text-foreground hover:bg-muted rounded-sm cursor-pointer outline-none font-sans"
								>
									<Settings class="size-4" />
									Settings
								</DropdownMenuItem>
								<DropdownMenuSeparator class="my-1 border-t border-border" />
								<DropdownMenuItem
									onclick={handleLogOut}
									class="flex items-center gap-2 px-2 py-1.5 text-sm text-red-650 hover:bg-red-500/10 dark:hover:bg-red-500/20 rounded-sm cursor-pointer outline-none font-sans"
								>
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
						onclick={showLogin}
						class="inline-flex h-9 items-center justify-center rounded-md border border-border bg-card px-4 text-xs font-semibold text-foreground hover:bg-muted transition-colors cursor-pointer select-none outline-none"
					>
						Login
					</button>
					<button
						onclick={showSignup}
						class="inline-flex h-9 items-center justify-center rounded-md bg-[#A16207] px-4 text-xs font-semibold text-primary-foreground hover:bg-[#A16207]/90 transition-colors shadow-xs cursor-pointer select-none outline-none"
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
			<div
				class="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-2xs"
			>
				<span class="size-2 rounded-full bg-[#C2410C] animate-pulse"></span>
				Powered by IBM Granite & LangGraph
			</div>
			<h1
				class="text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl lg:text-6xl font-sans"
			>
				Zentriom AI Powered Productivity and Career Assistant
			</h1>
			<p
				class="max-w-2xl mx-auto text-muted-foreground text-base sm:text-lg leading-relaxed font-sans"
			>
				An intelligent workspace powered by IBM Granite and LangGraph that helps students,
				developers, and professionals write better, understand code, fix bugs, create content, and
				discover career opportunities.
			</p>
			<div class="flex flex-wrap items-center justify-center gap-4 pt-4">
				{#if authStore.isAuthenticated}
					<a
						href="/dashboard"
						class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-primary-foreground hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
					>
						Dashboard
						<ChevronRight class="size-4 ml-1.5" />
					</a>
				{:else}
					<button
						onclick={showSignup}
						class="inline-flex h-11 items-center justify-center rounded-lg bg-[#A16207] px-6 text-sm font-semibold text-primary-foreground hover:bg-[#A16207]/90 transition-all shadow-sm cursor-pointer select-none outline-none"
					>
						Get Started
						<ChevronRight class="size-4 ml-1.5" />
					</button>
				{/if}
				<a
					href="#features"
					onclick={(e) => navigateToSection(e, 'features')}
					class="inline-flex h-11 items-center justify-center rounded-lg border border-border bg-card px-6 text-sm font-semibold text-foreground hover:bg-muted transition-all shadow-2xs"
				>
					Explore Features
				</a>
			</div>
		</div>
	</section>

	<!-- Authentication Section (Relocated above Toolkit) -->
	{#if !authStore.isAuthenticated}
		<section id="auth-section" class="py-16 px-4 sm:px-6 lg:px-8 border-t border-border bg-card/30">
			<div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
				<div class="space-y-6">
					<h2
						class="text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl font-sans leading-tight"
					>
						Experience the power of Granite AI
					</h2>
					<p class="text-muted-foreground font-sans text-sm sm:text-base leading-relaxed">
						Join developers and professionals who use Zentriom to automate their writing, analyze
						code, fix bugs, and track job matches in one unified environment.
					</p>
					<ul class="space-y-3">
						<li class="flex items-center gap-3 text-xs font-semibold text-foreground">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							IBM Granite & LangGraph under the hood
						</li>
						<li class="flex items-center gap-3 text-xs font-semibold text-foreground">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							Active code explainers and grammar fixer tools
						</li>
						<li class="flex items-center gap-3 text-xs font-semibold text-foreground">
							<span class="size-1.5 rounded-full bg-[#A16207]"></span>
							Zero-friction signup, get access instantly
						</li>
					</ul>
				</div>

				<div
					class="w-full max-w-md mx-auto rounded-2xl border border-border bg-card p-6 sm:p-8 shadow-sm space-y-6"
				>
					<div class="flex border-b border-border">
						<button
							onclick={() => (authTab = 'login')}
							class="flex-1 pb-3 text-sm font-bold text-center transition-all cursor-pointer outline-none select-none
								{authTab === 'login'
								? 'text-[#A16207] border-b-2 border-[#A16207]'
								: 'text-muted-foreground border-b-2 border-transparent hover:text-foreground'}"
						>
							Sign In
						</button>
						<button
							onclick={() => (authTab = 'signup')}
							class="flex-1 pb-3 text-sm font-bold text-center transition-all cursor-pointer outline-none select-none
								{authTab === 'signup'
								? 'text-[#A16207] border-b-2 border-[#A16207]'
								: 'text-muted-foreground border-b-2 border-transparent hover:text-foreground'}"
						>
							Create Account
						</button>
					</div>

					<div class="space-y-4">
						<div
							id="google-signin-button"
							class="w-full h-10 flex justify-center overflow-hidden rounded-lg"
						></div>

						<div class="relative flex py-1 items-center">
							<div class="flex-grow border-t border-border"></div>
							<span
								class="flex-shrink mx-4 text-[9px] font-bold text-muted-foreground uppercase tracking-wider"
							>
								OR CONTINUE WITH EMAIL
							</span>
							<div class="flex-grow border-t border-border"></div>
						</div>
					</div>

					{#if authTab === 'login'}
						<LoginForm />
					{:else}
						<SignUpForm />
					{/if}
				</div>
			</div>
		</section>
	{/if}

	<!-- Features Grid (Toolkit) -->
	<section id="features" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-border bg-card/30">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
					Comprehensive Toolkit
				</h2>
				<p class="text-muted-foreground text-xs sm:text-sm">
					Zentriom routes work automatically across specialized modules to boost outputs.
				</p>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each features as feat}
					{#if feat.underDevelopment}
						<div
							class="relative border border-border bg-card rounded-xl p-6 shadow-2xs opacity-70 select-none cursor-default"
						>
							<div
								class="absolute top-4 right-4 bg-muted text-muted-foreground border border-border text-[8px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full font-sans"
							>
								UNDER DEVELOPMENT
							</div>
							<div class="p-2.5 rounded-lg bg-background text-muted-foreground w-fit mb-4">
								<feat.icon class="size-5 shrink-0" />
							</div>
							<h3 class="text-base font-bold text-muted-foreground/80 mb-2">{feat.name}</h3>
							<p class="text-muted-foreground text-xs leading-relaxed font-sans">{feat.desc}</p>
						</div>
					{:else}
						<button
							onclick={(e) => {
								if (authStore.isAuthenticated) {
									goto(feat.path);
								} else {
									e.preventDefault();
									showLogin();
								}
							}}
							class="text-left w-full group block border border-border bg-card rounded-xl p-6 shadow-2xs hover:border-[#A16207]/30 transition-all hover:shadow-xs outline-none cursor-pointer"
						>
							<div
								class="p-2.5 rounded-lg bg-muted text-foreground group-hover:bg-[#A16207]/10 group-hover:text-[#A16207] transition-all w-fit mb-4"
							>
								<feat.icon class="size-5 shrink-0" />
							</div>
							<h3
								class="text-base font-bold text-foreground mb-2 group-hover:text-[#A16207] transition-all"
							>
								{feat.name}
							</h3>
							<p class="text-muted-foreground text-xs leading-relaxed font-sans">{feat.desc}</p>
						</button>
					{/if}
				{/each}
			</div>
		</div>
	</section>

	<!-- How It Works Section -->
	<section id="how-it-works" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-border">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-foreground sm:text-3xl font-sans">
					How It Works
				</h2>
				<p class="text-muted-foreground text-xs sm:text-sm font-sans">
					Seamless workflow routing designed for single-user workspaces.
				</p>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 relative">
				{#each steps as step}
					<div
						class="relative border border-border/80 hover:border-[#A16207]/30 bg-card rounded-2xl p-6 shadow-2xs hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 ease-out group"
					>
						{#if step.step !== '04'}
							<div
								class="hidden lg:block absolute top-[3.25rem] left-full w-6 border-t border-dashed border-border/80 z-20"
							></div>
						{/if}
						<div
							class="relative w-14 h-14 flex items-center justify-center rounded-2xl bg-[#A16207]/10 border border-[#A16207]/20 mb-5 shadow-[0_0_15px_-3px_rgba(161,98,7,0.1)] transition-colors duration-300 group-hover:bg-[#A16207]/15 group-hover:border-[#A16207]/35 select-none"
						>
							<span class="text-2xl font-black text-[#A16207] tracking-tight font-sans"
								>{step.step}</span
							>
						</div>
						<h3 class="text-sm font-extrabold text-foreground tracking-tight mb-1.5 font-sans">
							{step.title}
						</h3>
						<p class="text-muted-foreground text-xs leading-relaxed font-sans">{step.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Why Zentriom Section -->
	<section id="why-zentriom" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-border bg-card/30">
		<div class="max-w-7xl mx-auto space-y-12">
			<div class="text-center max-w-xl mx-auto space-y-2">
				<h2 class="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">Why Zentriom</h2>
				<p class="text-muted-foreground text-xs sm:text-sm">
					Designed specifically to enhance your personal flow.
				</p>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
				{#each benefits as ben}
					<div class="border border-border bg-card rounded-xl p-6 shadow-2xs">
						<h3 class="text-sm font-bold text-foreground mb-1.5">{ben.title}</h3>
						<p class="text-muted-foreground text-xs leading-relaxed font-sans">{ben.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Footer -->
	<footer
		class="border-t border-border py-8 px-4 sm:px-6 lg:px-8 text-center text-muted-foreground text-[11px]"
	>
		<p>
			© {new Date().getFullYear()} Zentriom AI. Built with IBM Granite &amp; LangGraph. All rights reserved.
		</p>
	</footer>
</div>
