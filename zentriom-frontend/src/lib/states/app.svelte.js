import { authStore } from "$lib/stores/auth.svelte.js";

export const appState = $state({
	sidebarCollapsed: false,
	mobileSidebarOpen: false,
	pageTitle: "Dashboard",
	currentRoute: "/dashboard",
	get user() {
		return authStore.user;
	},
	set user(value) {
		authStore.user = value;
	}
});
