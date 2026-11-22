import { expect, test } from "@playwright/test";

test("home loads the backend status", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByTestId("api-status")).toContainText("Hello World!");
  await expect(
    page.getByRole("main").getByRole("link", { name: "API docs" }),
  ).toHaveAttribute("href", "/api/docs");
});
