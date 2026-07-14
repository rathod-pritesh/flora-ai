<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/dashboard');
	});
</script>

<div class="flex items-center justify-center min-h-[400px]">
	<p class="text-stone-500 font-sans text-sm animate-pulse">Redirecting...</p>
</div>
