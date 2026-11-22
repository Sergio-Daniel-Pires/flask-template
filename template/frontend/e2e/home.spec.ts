import { expect, test } from "@playwright/test";

test("home data, navigation and deep links work", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByTestId("api-status")).toContainText("Hello World!");

  await page.getByRole("link", { name: "Sobre" }).click();
  await expect(page.getByRole("heading", { name: "Sobre" })).toBeVisible();

  // Direct load is handled by the Flask SPA fallback.
  await page.goto("/about");
  await expect(page.getByRole("heading", { name: "Sobre" })).toBeVisible();
});
