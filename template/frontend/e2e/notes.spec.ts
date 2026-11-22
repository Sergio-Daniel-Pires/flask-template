import { expect, test } from "@playwright/test";

test("creates a note and lists it", async ({ page }) => {
  const text = `Nota E2E ${Date.now()}`;

  await page.goto("/notes");
  await page.getByLabel("Nova nota").fill(text);
  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByTestId("notes-list")).toContainText(text);
});
