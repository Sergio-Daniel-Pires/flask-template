import { expect, test } from "@playwright/test";

test("creates a note and lists it", async ({ page }) => {
  const text = `E2E note ${Date.now()}`;

  await page.goto("/notes");
  await page.getByLabel("New note").fill(text);
  await page.getByRole("button", { name: "Add" }).click();

  await expect(page.getByTestId("notes-list")).toContainText(text);
});
