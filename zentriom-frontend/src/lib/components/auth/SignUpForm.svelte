<script>
	import { Eye, EyeOff } from 'lucide-svelte';
	import { sendSignupOtp, verifySignupOtp, register } from '$lib/services/auth';
	import { setAuth } from '$lib/stores/auth.svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	let fullName = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let showPassword = $state(false);

	// Validation / UI States
	let nameTouched = $state(false);
	let emailTouched = $state(false);
	let passwordTouched = $state(false);
	let confirmTouched = $state(false);

	let signupState = $state('details'); // 'details' | 'otp' | 'verified'
	let otpValues = $state(['', '', '', '']);
	let otpInputs = [];

	let isSendingOtp = $state(false);
	let isVerifyingOtp = $state(false);
	let isRegistering = $state(false);

	// Derived validation messages
	const nameErrorMsg = $derived(
		!fullName.trim() ? (nameTouched ? 'Full name is required' : '') : ''
	);

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

	const confirmErrorMsg = $derived(
		confirmTouched && password !== confirmPassword ? 'Passwords do not match' : ''
	);

	const isDetailsInvalid = $derived(
		!fullName.trim() ||
			!email.trim() ||
			!/\S+@\S+\.\S+/.test(email)
	);

	const isOtpInvalid = $derived(
		otpValues.some((v) => !v)
	);

	const isRegisterInvalid = $derived(
		!password || password !== confirmPassword
	);

	async function handleSendVerification(e) {
		if (e) e.preventDefault();
		nameTouched = true;
		emailTouched = true;
		if (isDetailsInvalid) return;

		isSendingOtp = true;
		try {
			await sendSignupOtp(fullName, email);
			toast.success('Verification code sent.');
			signupState = 'otp';
		} catch (error) {
			toast.error(error.message || 'Unable to send verification code.');
		} finally {
			isSendingOtp = false;
		}
	}

	function handleOtpInput(index, event) {
		const val = event.target.value;
		const char = val.slice(-1);
		otpValues[index] = char;

		if (char && index < 3) {
			otpInputs[index + 1]?.focus();
		}
	}

	function handleOtpKeyDown(index, event) {
		if (event.key === 'Backspace' && !otpValues[index] && index > 0) {
			otpInputs[index - 1]?.focus();
		}
	}

	async function handleVerifyEmail(e) {
		if (e) e.preventDefault();
		if (isOtpInvalid) return;

		isVerifyingOtp = true;
		try {
			await verifySignupOtp(email, otpValues.join(''));
			toast.success('Email verified successfully.');
			signupState = 'verified';
		} catch (error) {
			toast.error(error.message || 'Invalid verification code.');
		} finally {
			isVerifyingOtp = false;
		}
	}

	async function handleRegister(e) {
		if (e) e.preventDefault();
		passwordTouched = true;
		confirmTouched = true;
		if (isRegisterInvalid) return;

		isRegistering = true;
		try {
			const result = await register(fullName, email, password);
			setAuth(result.user, result.token);
			toast.success('Account created successfully.');
			goto('/dashboard');
		} catch (error) {
			toast.error(error.message || 'Registration failed.');
		} finally {
			isRegistering = false;
		}
	}
</script>

<form 
	onsubmit={signupState === 'details' ? handleSendVerification : (signupState === 'otp' ? handleVerifyEmail : handleRegister)} 
	class="space-y-4"
>
	<!-- Full Name Field -->
	<div class="space-y-1">
		<label
			for="signup-name"
			class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
			>Full Name</label
		>
		<input
			id="signup-name"
			type="text"
			bind:value={fullName}
			disabled={signupState !== 'details'}
			onblur={() => (nameTouched = true)}
			placeholder="e.g. John Doe"
			class="w-full h-10 px-3 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs disabled:opacity-60 disabled:cursor-not-allowed
				{nameErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
		/>
		{#if nameErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{nameErrorMsg}</p>
		{/if}
	</div>

	<!-- Email Field -->
	<div class="space-y-1">
		<div class="flex items-center justify-between">
			<label
				for="signup-email"
				class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
				>Email Address</label
			>
			{#if signupState === 'verified'}
				<span class="inline-flex items-center gap-1 text-[9px] font-bold text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full uppercase tracking-wider font-sans">
					Verified
				</span>
			{/if}
		</div>
		<input
			id="signup-email"
			type="email"
			bind:value={email}
			disabled={signupState !== 'details'}
			onblur={() => (emailTouched = true)}
			placeholder="e.g. johndoe@example.com"
			class="w-full h-10 px-3 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs disabled:opacity-60 disabled:cursor-not-allowed
				{emailErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
		/>
		{#if emailErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{emailErrorMsg}</p>
		{/if}
	</div>

	<!-- OTP Field -->
	{#if signupState === 'otp'}
		<div class="space-y-2">
			<label
				for="verificationcode"
				class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
				>Enter Verification Code</label
			>

			<div class="flex justify-between gap-2 max-w-xs mx-auto">
				{#each [0, 1, 2, 3] as index}
					<input
						type="text"
						maxlength="1"
						bind:this={otpInputs[index]}
						value={otpValues[index]}
						oninput={(e) => handleOtpInput(index, e)}
						onkeydown={(e) => handleOtpKeyDown(index, e)}
						class="w-12 h-12 text-center text-lg font-bold border border-border rounded-lg bg-card text-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans"
					/>
				{/each}
			</div>
		</div>
	{/if}

	<!-- Password / Registration Fields -->
	{#if signupState === 'verified'}
		<!-- Password Field -->
		<div class="space-y-1">
			<label
				for="signup-password"
				class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
				>Password</label
			>
			<div class="relative">
				<input
					id="signup-password"
					type={showPassword ? 'text' : 'password'}
					bind:value={password}
					onblur={() => (passwordTouched = true)}
					placeholder="••••••••"
					class="w-full h-10 pl-3 pr-10 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
						{passwordErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
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

		<!-- Confirm Password Field -->
		<div class="space-y-1">
			<label
				for="signup-confirm-password"
				class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
				>Confirm Password</label
			>
			<input
				id="signup-confirm-password"
				type="password"
				bind:value={confirmPassword}
				onblur={() => (confirmTouched = true)}
				placeholder="••••••••"
				class="w-full h-10 px-3 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
					{confirmErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
			/>
			{#if confirmErrorMsg}
				<p class="text-red-500 text-[10px] font-semibold">{confirmErrorMsg}</p>
			{/if}
		</div>
	{/if}

	<!-- Submit Buttons -->
	{#if signupState === 'details'}
		<button
			type="submit"
			disabled={isDetailsInvalid || isSendingOtp}
			class="w-full h-11 bg-[#A16207] text-primary-foreground rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
				{isDetailsInvalid || isSendingOtp ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
		>
			<span>{isSendingOtp ? 'Sending...' : 'Send Verification Code'}</span>
		</button>
	{:else if signupState === 'otp'}
		<button
			type="submit"
			disabled={isOtpInvalid || isVerifyingOtp}
			class="w-full h-11 bg-[#A16207] text-primary-foreground rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
				{isOtpInvalid || isVerifyingOtp ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
		>
			<span>{isVerifyingOtp ? 'Verifying...' : 'Verify Email'}</span>
		</button>
	{:else if signupState === 'verified'}
		<button
			type="submit"
			disabled={isRegisterInvalid || isRegistering}
			class="w-full h-11 bg-[#A16207] text-primary-foreground rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
				{isRegisterInvalid || isRegistering ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
		>
			<span>{isRegistering ? 'Creating Account...' : 'Create Account'}</span>
		</button>
	{/if}
</form>
