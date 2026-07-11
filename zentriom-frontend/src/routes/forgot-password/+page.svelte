<script>
	import { goto } from '$app/navigation';
	import { ArrowLeft } from 'lucide-svelte';
	import { forgotPassword, verifyOtp } from '$lib/services/auth';

	let email = $state('');
	let emailTouched = $state(false);
	let otpSent = $state(false);
	let otpValues = $state(['', '', '', '']);
	let otpInputs = [];

	let errorMessage = $state('');

	const emailErrorMsg = $derived(
		!email.trim()
			? emailTouched
				? 'Email address is required'
				: ''
			: !/\S+@\S+\.\S+/.test(email)
				? 'Please enter a valid email address'
				: ''
	);

	async function handleSendOtp(e) {
		if (e) e.preventDefault();
		emailTouched = true;
		if (emailErrorMsg || !email.trim()) return;

		try {
			errorMessage = '';

			await forgotPassword(email);

			otpSent = true;
		} catch (error) {
			errorMessage = error.message;
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

	async function handleVerifyOtp(e) {
		if (e) e.preventDefault();
		if (otpValues.some((v) => !v)) return;

		try {
			errorMessage = '';

			const otp = otpValues.join('');

			await verifyOtp(email, otp);

			sessionStorage.setItem('reset_email', email);

			sessionStorage.setItem('reset_otp', otp);

			goto('/reset-password');
		} catch (error) {
			errorMessage = error.message;
		}
	}
</script>

<div
	class="min-h-screen bg-[#F8F7F4] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 text-[#1C1917] font-sans selection:bg-[#A16207]/20 selection:text-[#A16207]"
>
	<div class="sm:mx-auto sm:w-full sm:max-w-md text-center mb-6">
		<div class="flex items-center justify-center gap-3">
			<img src="/zentriom_logo_for_dark_theme.png" class="size-11 object-contain" alt="Zentriom" />
			<span class="text-xl font-bold tracking-tight text-[#1C1917] font-sans">
				<a href="/">Zentriom</a>
			</span>
		</div>
	</div>

	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<div class="bg-white py-8 px-6 shadow-sm border border-[#E7E5E4] rounded-2xl space-y-6">
			<div class="space-y-2">
				<h2 class="text-xl font-bold text-stone-900 font-sans">Forgot Password</h2>
				<p class="text-xs text-stone-500 font-sans leading-relaxed">
					Enter your registered email address to receive a verification code.
				</p>
			</div>

			{#if !otpSent}
				<form onsubmit={handleSendOtp} class="space-y-4">
					<div class="space-y-1">
						<label
							for="forgot-email"
							class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans"
							>Email Address</label
						>
						<input
							id="forgot-email"
							type="email"
							bind:value={email}
							onblur={() => (emailTouched = true)}
							placeholder="e.g. pritesh@example.com"
							class="w-full h-10 px-3 rounded-lg border bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
								{emailErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-stone-200'}"
						/>
						{#if emailErrorMsg}
							<p class="text-red-500 text-[10px] font-semibold">{emailErrorMsg}</p>
						{/if}
					</div>

					<button
						type="submit"
						disabled={!email.trim() || !!emailErrorMsg}
						class="w-full h-11 bg-[#A16207] text-[#F8F7F4] rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
							{!email.trim() || !!emailErrorMsg ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
					>
						Send OTP
					</button>
				</form>
			{:else}
				<form onsubmit={handleVerifyOtp} class="space-y-4">
					<div class="space-y-2">
						<label
							class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans"
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
									class="w-12 h-12 text-center text-lg font-bold border border-stone-200 rounded-lg bg-[#FDFCFB] text-stone-900 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans"
								/>
							{/each}
						</div>
					</div>

					<button
						type="submit"
						disabled={otpValues.some((v) => !v)}
						class="w-full h-11 bg-[#A16207] text-[#F8F7F4] rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
							{otpValues.some((v) => !v) ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
					>
						Verify OTP
					</button>
				</form>
			{/if}

			<div class="text-center pt-2">
				<a
					href="/?showAuth=true"
					class="inline-flex items-center gap-1.5 text-xs text-[#A16207] font-semibold hover:underline outline-none"
				>
					<ArrowLeft class="size-3.5" />
					<span>Back to Sign In</span>
				</a>

				{#if errorMessage}
					<p class="text-red-500 text-xs">
						{errorMessage}
					</p>
				{/if}
			</div>
		</div>
	</div>
</div>
