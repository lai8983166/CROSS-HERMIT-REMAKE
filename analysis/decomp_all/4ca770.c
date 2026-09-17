
void FUN__text__004ca770(short param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined1 *puVar5;
  undefined4 uVar6;
  undefined4 local_14c [16];
  undefined1 local_10c [204];
  undefined4 uStack_40;
  undefined2 local_c;
  int local_8;
  
  puVar4 = local_14c;
  for (iVar3 = 0x52; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (param_1 < 0) {
    local_c = 0;
  }
  (*API_GDI32_DLL_CreateFontA)(0x14,0,0,0,700,0,0,0,1,5,0,0,0,&DAT_005bf62c);
  uVar1 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x5c) = uVar1;
  FUN__text__0056d810(local_10c,(&PTR_DAT_00621f2c)[param_1]);
  FUN__text__004077c0(DAT_007a49fc);
  uVar6 = 2;
  puVar5 = local_10c;
  uVar1 = *(undefined4 *)(local_8 + 0x5c);
  uVar2 = FUN__text__004142b0(uVar1,puVar5,2);
  FUN__text__00408e30(uVar2,uVar1,puVar5,uVar6);
  FUN__text__004d1bf0(local_8 + 0x5c);
  uStack_40 = 0x4ca84f;
  FUN__text__0056ce80();
  return;
}

