<script>
	import '../app.css';
	import { Toaster } from 'svelte-sonner';
	import { themeStore } from '$lib/stores/theme.svelte.js';

	let { children } = $props();
</script>

<Toaster richColors />

{@render children?.()}
