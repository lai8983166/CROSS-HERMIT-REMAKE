
void FUN__text__004c7f80(undefined4 param_1)

{
  undefined2 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined1 *puVar6;
  undefined4 uVar7;
  undefined4 local_b78 [16];
  undefined4 local_b38;
  int local_b34 [10];
  undefined1 auStack_b0c [2552];
  undefined1 local_114 [256];
  short local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar5 = local_b78;
  for (iVar4 = 0x2dd; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_c = 10;
  local_10 = 0x14;
  (*API_GDI32_DLL_CreateFontA)(0x14,10,0,0,400,0,0,0,1,5,0,0,0,&DAT_005bf62c);
  uVar2 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x2c + *(short *)(local_8 + 10) * 0x298) = uVar2;
  local_14 = 0;
  local_b38 = (uint)local_b38._2_2_ << 0x10;
  while ((local_b38 & 0xffff) < 10) {
    local_b34[local_b38 & 0xffff] = (int)(auStack_b0c + (local_b38 & 0xffff) * 0xff);
    local_b38 = CONCAT22(local_b38._2_2_,(short)local_b38 + 1);
  }
  uVar1 = FUN__text__004cd5b0(param_1,local_b34);
  *(undefined2 *)(local_8 + 0x2a + *(short *)(local_8 + 10) * 0x298) = uVar1;
  for (local_14 = 0; local_14 < *(short *)(local_8 + 0x2a + *(short *)(local_8 + 10) * 0x298);
      local_14 = local_14 + 1) {
    FUN__text__0056d810(local_114,local_b34[local_14]);
    FUN__text__004077c0(DAT_007a49fc);
    uVar7 = 2;
    puVar6 = local_114;
    uVar2 = *(undefined4 *)(local_8 + 0x2c + *(short *)(local_8 + 10) * 0x298);
    uVar3 = FUN__text__004142b0(uVar2,puVar6,2);
    FUN__text__00408e30(uVar3,uVar2,puVar6,uVar7);
  }
  FUN__text__004d1bf0(local_8 + 0x2c + *(short *)(local_8 + 10) * 0x298);
  *(undefined2 *)(local_8 + 0x1a + *(short *)(local_8 + 10) * 0x298) =
       *(undefined2 *)(local_8 + 0x14);
  *(undefined2 *)(local_8 + 0x1c + *(short *)(local_8 + 10) * 0x298) =
       *(undefined2 *)(local_8 + 0x16);
  *(undefined2 *)(local_8 + 0x1e + *(short *)(local_8 + 10) * 0x298) = 400;
  *(short *)(local_8 + 0x20 + *(short *)(local_8 + 10) * 0x298) =
       *(short *)(local_8 + 0x2a + *(short *)(local_8 + 10) * 0x298) * 0x16 + -2;
  *(undefined2 *)(local_8 + 0x18 + *(short *)(local_8 + 10) * 0x298) = 1;
  *(undefined2 *)(local_8 + 0x22 + *(short *)(local_8 + 10) * 0x298) = 0x10;
  *(short *)(local_8 + 0x16) =
       *(short *)(local_8 + 0x16) +
       *(short *)(local_8 + 0x2a + *(short *)(local_8 + 10) * 0x298) * 0x16;
  *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
  local_8 = 0x4c828a;
  FUN__text__0056ce80();
  return;
}

