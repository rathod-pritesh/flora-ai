<script>
	import { goto } from '$app/navigation';
	import { resetPassword } from '$lib/services/auth';
	import { ArrowLeft, Eye, EyeOff } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';

	let password = $state('');
	let confirmPassword = $state('');
	let passwordTouched = $state(false);
	let confirmTouched = $state(false);

	let showPassword = $state(false);
	let showConfirmPassword = $state(false);

	let errorMessage = $state('');
	let successMessage = $state('');

	const passwordErrorMsg = $derived(
		!password ? (passwordTouched ? 'Password is required' : '') : ''
	);

	const confirmErrorMsg = $derived(
		confirmTouched && password !== confirmPassword ? 'Passwords do not match' : ''
	);

	const isFormInvalid = $derived(!password || !confirmPassword || password !== confirmPassword);

	async function handleSubmit(e) {
		if (e) e.preventDefault();
		passwordTouched = true;
		confirmTouched = true;

		if (isFormInvalid) return;

		try {
			errorMessage = '';

			const email = sessionStorage.getItem('reset_email');

			const otp = sessionStorage.getItem('reset_otp');

			if (!email || !otp) {
				throw new Error('Session expired. Start again.');
			}

			await resetPassword(email, otp, password);

			sessionStorage.removeItem('reset_email');

			sessionStorage.removeItem('reset_otp');

			successMessage = 'Password changed successfully';
			toast.success('Password updated successfully.');

			setTimeout(() => {
				goto('/?showAuth=true');
			}, 1500);
		} catch (error) {
			errorMessage = error.message;
			toast.error(error.message || 'Password reset failed.');
		}
	}
</script>

<div
	class="min-h-screen bg-background flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 text-foreground font-sans selection:bg-[#A16207]/20 selection:text-[#A16207]"
>
	<div class="sm:mx-auto sm:w-full sm:max-w-md text-center mb-6">
		<div class="flex items-center justify-center gap-3">
			<img src="/logo.png" class="size-11 object-contain" alt="Zentriom" />
			<span class="text-xl font-bold tracking-tight text-foreground font-sans">
				<a href="/">Zentriom</a>
			</span>
		</div>
	</div>

	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<div class="bg-card py-8 px-6 shadow-sm border border-border rounded-2xl space-y-6">
			<div class="space-y-2">
				<h2 class="text-xl font-bold text-foreground font-sans">Reset Password</h2>
				<p class="text-xs text-muted-foreground font-sans leading-relaxed">
					Create a new password for your account.
				</p>
			</div>

			{#if successMessage}
				<div
					class="p-3 bg-emerald-50 text-emerald-800 text-xs rounded-lg border border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20"
				>
					{successMessage}
				</div>
			{/if}

			{#if errorMessage}
				<div
					class="p-3 bg-red-50 text-red-700 text-xs rounded-lg border border-red-200 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20"
				>
					{errorMessage}
				</div>
			{/if}

			<form onsubmit={handleSubmit} class="space-y-4">
				<!-- Password Field -->
				<div class="space-y-1">
					<label
						for="reset-password"
						class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
						>New Password</label
					>
					<div class="relative">
						<input
							id="reset-password"
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
						for="reset-confirm"
						class="block text-[10px] font-bold text-muted-foreground tracking-wider uppercase font-sans"
						>Confirm New Password</label
					>
					<div class="relative">
						<input
							id="reset-confirm"
							type={showConfirmPassword ? 'text' : 'password'}
							bind:value={confirmPassword}
							onblur={() => (confirmTouched = true)}
							placeholder="••••••••"
							class="w-full h-10 pl-3 pr-10 rounded-lg border bg-card text-foreground placeholder:text-muted-foreground focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
								{confirmErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-border'}"
						/>
						<button
							type="button"
							onclick={() => (showConfirmPassword = !showConfirmPassword)}
							class="absolute right-3 top-3 text-muted-foreground hover:text-foreground outline-none cursor-pointer"
						>
							{#if showConfirmPassword}
								<EyeOff class="size-3.5" />
							{:else}
								<Eye class="size-3.5" />
							{/if}
						</button>
					</div>
					{#if confirmErrorMsg}
						<p class="text-red-500 text-[10px] font-semibold">{confirmErrorMsg}</p>
					{/if}
				</div>

				<button
					type="submit"
					disabled={isFormInvalid}
					class="w-full h-11 bg-[#A16207] text-primary-foreground rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
						{isFormInvalid ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
				>
					Reset Password
				</button>
			</form>

			<div class="text-center pt-2">
				<a
					href="/?showAuth=true"
					class="inline-flex items-center gap-1.5 text-xs text-[#A16207] font-semibold hover:underline outline-none"
				>
					<ArrowLeft class="size-3.5" />
					<span>Back to Sign In</span>
				</a>
			</div>
		</div>
	</div>
</div>
