let defaultUser = {
	name: "",
	email: "",
	title: "",
	skills: [],
	preferences: {
		location: "",
		remote: "Remote",
		jobType: "Full-time"
	}
};

if (typeof window !== 'undefined') {
	const saved = localStorage.getItem('zentriom_user');
	if (saved) {
		try {
			defaultUser = JSON.parse(saved);
		} catch (e) {}
	}
}

export const appState = $state({
	sidebarCollapsed: false,
	mobileSidebarOpen: false,
	pageTitle: "Dashboard",
	currentRoute: "/dashboard",
	user: defaultUser
});
