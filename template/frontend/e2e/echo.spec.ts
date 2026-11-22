import { expect, test } from "@playwright/test";

test("echoes reversed and mirrored messages", async ({ page }) => {
  await page.goto("/echo");

  await page.getByLabel("Message").fill("Hello");
  await page.getByLabel("Echo type").selectOption("Reverse");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByTestId("echo-result")).toHaveText("olleH");

  await page.getByLabel("Echo type").selectOption("Mirror");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByTestId("echo-result")).toHaveText("Hello | olleH");
});
