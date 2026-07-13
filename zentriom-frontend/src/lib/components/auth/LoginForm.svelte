<script>
	import { Eye, EyeOff } from 'lucide-svelte';
	import { login } from '$lib/services/auth';
	import { setAuth } from '$lib/stores/auth.svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	let email = $state('');
	let password = $state('');
	let showPassword = $state(false);

	// Validation / UI States
	let emailTouched = $state(false);
	let passwordTouched = $state(false);

	// Derived inline validation messages
	const emailErrorMsg = $derived(
		!email.trim()
			? emailTouched
				? 'Email address is required'
				: ''
			: !/\S+@\S+\.\S+/.test(email)
				? 'Please enter a valid email address'
				: ''
	);

	const passwordErrorMsg = $derived(
		!password ? (passwordTouched ? 'Password is required' : '') : ''
	);

	const isFormInvalid = $derived(!email.trim() || !/\S+@\S+\.\S+/.test(email) || !password);

	async function handleSubmit(e) {
		if (e) e.preventDefault();

		emailTouched = true;
		passwordTouched = true;

		if (isFormInvalid) return;

		try {
			const result = await login(email, password);

			setAuth(result.user, result.token);

			toast.success('Welcome back!');

			goto('/dashboard');

		} catch (error) {
			toast.error(error.message || 'Invalid email or password');
		}
	}
</script>

<form onsubmit={handleSubmit} class="space-y-4">
	
	<!-- Email Field -->
	<div class="space-y-1">
		<label
			for="login-email"
			class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
			>Email Address</label
		>
		<input
			id="login-email"
			type="email"
			bind:value={email}
			onblur={() => (emailTouched = true)}
			placeholder="e.g. pritesh@example.com"
			class="w-full h-10 px-3 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
				{emailErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
		/>
		{#if emailErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{emailErrorMsg}</p>
		{/if}
	</div>

	<!-- Password Field -->
	<div class="space-y-1">
		<div class="flex justify-between items-center">
			<label
				for="login-password"
				class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
				>Password</label
			>
			<a
				href="/forgot-password"
				class="text-[10px] text-[#A16207] font-semibold hover:underline outline-none cursor-pointer"
			>
				Forgot Password?
			</a>
		</div>
		<div class="relative">
			<input
				id="login-password"
				type={showPassword ? 'text' : 'password'}
				bind:value={password}
				onblur={() => (passwordTouched = true)}
				placeholder="••••••••"
				class="w-full h-10 pl-3 pr-10 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
					{passwordErrorMsg
					? 'border-red-500 focus:border-red-500 focus:ring-red-500/20'
					: 'border-border'}"
			/>
			<button
				type="button"
				onclick={() => (showPassword = !showPassword)}
				class="absolute right-3 top-3 text-muted-foreground hover:text-foreground outline-none cursor-pointer"
			>
				{#if showPassword}
					<EyeOff class="size-3.5" />
				{:else}
					<Eye class="size-3.5" />
				{/if}
			</button>
		</div>
		{#if passwordErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{passwordErrorMsg}</p>
		{/if}
	</div>

	<button
		type="submit"
		disabled={isFormInvalid}
		class="w-full h-11 bg-[#A16207] text-primary-foreground rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
			{isFormInvalid ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
	>
		<span>Sign In</span>
	</button>
</form>
