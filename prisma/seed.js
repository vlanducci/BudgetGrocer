import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  await prisma.store.upsert({
    where: { id: 1 },
    update: {},
    create: {
      id: 1,
      name: "Aldi",
    },
  });

  await prisma.store.upsert({
    where: { id: 2 },
    update: {},
    create: {
      id: 2,
      name: "Coles",
    },
  });

  await prisma.store.upsert({
    where: { id: 3 },
    update: {},
    create: {
      id: 3,
      name: "Woolworths",
    },
  });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });