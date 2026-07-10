<script>
	import { Eye, EyeOff } from "lucide-svelte";

	let fullName = $state("");
	let email = $state("");
	let password = $state("");
	let confirmPassword = $state("");
	let showPassword = $state(false);
	
	// Validation / UI States
	let nameTouched = $state(false);
	let emailTouched = $state(false);
	let passwordTouched = $state(false);
	let confirmTouched = $state(false);
	let successMsg = $state("");

	// Derived validation messages
	const nameErrorMsg = $derived(
		!fullName.trim() ? (nameTouched ? "Full name is required" : "") : ""
	);

	const emailErrorMsg = $derived(
		!email.trim()
			? (emailTouched ? "Email address is required" : "")
			: (!/\S+@\S+\.\S+/.test(email) ? "Please enter a valid email address" : "")
	);

	const passwordErrorMsg = $derived(
		!password ? (passwordTouched ? "Password is required" : "") : ""
	);

	const confirmErrorMsg = $derived(
		confirmTouched && password !== confirmPassword ? "Passwords do not match" : ""
	);

	const isFormInvalid = $derived(
		!fullName.trim() || !email.trim() || !/\S+@\S+\.\S+/.test(email) || !password || password !== confirmPassword
	);

	function handleSubmit(e) {
		if (e) e.preventDefault();
		
		// Touch all fields on submit
		nameTouched = true;
		emailTouched = true;
		passwordTouched = true;
		confirmTouched = true;
		successMsg = "";

		if (isFormInvalid) return;

		// Pure UI submission - emit values or display status
		successMsg = `Registration submitted successfully for ${fullName}. Ready for backend connection.`;
	}
</script>

<form onsubmit={handleSubmit} class="space-y-4">
	<!-- Success Banner
	{#if successMsg}
		<div class="p-3 bg-emerald-50 text-emerald-800 text-xs rounded-lg border border-emerald-250 font-medium">
			{successMsg}
		</div>
	{/if} -->

	<!-- Full Name Field -->
	<div class="space-y-1">
		<label for="signup-name" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Full Name</label>
		<input
			id="signup-name"
			type="text"
			bind:value={fullName}
			onblur={() => nameTouched = true}
			placeholder="e.g. Pritesh Rathod"
			class="w-full h-10 px-3 rounded-lg border bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
				{nameErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-stone-200'}"
		/>
		{#if nameErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{nameErrorMsg}</p>
		{/if}
	</div>

	<!-- Email Field -->
	<div class="space-y-1">
		<label for="signup-email" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Email Address</label>
		<input
			id="signup-email"
			type="email"
			bind:value={email}
			onblur={() => emailTouched = true}
			placeholder="e.g. pritesh@example.com"
			class="w-full h-10 px-3 rounded-lg border bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
				{emailErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-stone-200'}"
		/>
		{#if emailErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{emailErrorMsg}</p>
		{/if}
	</div>

	<!-- Password Field -->
	<div class="space-y-1">
		<label for="signup-password" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Password</label>
		<div class="relative">
			<input
				id="signup-password"
				type={showPassword ? "text" : "password"}
				bind:value={password}
				onblur={() => passwordTouched = true}
				placeholder="••••••••"
				class="w-full h-10 pl-3 pr-10 rounded-lg border bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
					{passwordErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-stone-200'}"
			/>
			<button
				type="button"
				onclick={() => showPassword = !showPassword}
				class="absolute right-3 top-3 text-stone-455 hover:text-stone-700 outline-none cursor-pointer"
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
		<label for="signup-confirm-password" class="block text-[10px] font-bold text-stone-700 tracking-wider uppercase font-sans">Confirm Password</label>
		<input
			id="signup-confirm-password"
			type="password"
			bind:value={confirmPassword}
			onblur={() => confirmTouched = true}
			placeholder="••••••••"
			class="w-full h-10 px-3 rounded-lg border bg-[#FDFCFB] text-stone-900 placeholder-stone-400 focus:outline-hidden focus:border-[#A16207] focus:ring-1 focus:ring-[#A16207]/30 transition-all font-sans text-xs
				{confirmErrorMsg ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-stone-200'}"
		/>
		{#if confirmErrorMsg}
			<p class="text-red-500 text-[10px] font-semibold">{confirmErrorMsg}</p>
		{/if}
	</div>

	<button
		type="submit"
		disabled={isFormInvalid}
		class="w-full h-11 bg-[#A16207] text-[#F8F7F4] rounded-lg hover:bg-[#A16207]/90 transition-all text-xs font-bold cursor-pointer select-none outline-none shadow-sm flex items-center justify-center gap-2
			{isFormInvalid ? 'opacity-60 pointer-events-none cursor-not-allowed' : ''}"
	>
		<span>Create Account</span>
	</button>
</form>
