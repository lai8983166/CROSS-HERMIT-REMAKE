
void __thiscall FUN__text__004cabd0(int param_1,undefined4 param_2,undefined2 param_3)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined1 *puVar6;
  undefined4 uVar7;
  undefined4 local_154 [16];
  undefined1 local_114 [256];
  undefined4 local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_154;
  for (iVar3 = 0x54; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (9 < *(ushort *)(param_1 + 0x16)) {
    *(undefined2 *)(param_1 + 0x16) = 9;
  }
  *(undefined2 *)(param_1 + 0x18 + (uint)*(ushort *)(param_1 + 0x16) * 0x110) = 2;
  *(undefined2 *)(param_1 + 0x1a + (uint)*(ushort *)(param_1 + 0x16) * 0x110) = 0;
  local_8 = param_1;
  uVar1 = FUN__text__004cafa0();
  *(undefined2 *)(local_8 + 0x1c + (uint)*(ushort *)(local_8 + 0x16) * 0x110) = uVar1;
  *(undefined2 *)(local_8 + 0x1e + (uint)*(ushort *)(local_8 + 0x16) * 0x110) = 0;
  *(undefined2 *)(local_8 + 0x20 + (uint)*(ushort *)(local_8 + 0x16) * 0x110) = param_3;
  *(undefined2 *)(local_8 + 0x24 + (uint)*(ushort *)(local_8 + 0x16) * 0x110) = 0x16;
  *(undefined2 *)(local_8 + 0x22 + (uint)*(ushort *)(local_8 + 0x16) * 0x110) = 0;
  local_c = FUN__text__004cb180();
  local_10 = FUN__text__004cb1d0();
  (*API_GDI32_DLL_CreateFontA)((int)local_10,(int)local_c,0,0,400,0,0,0,1,5,0,0,0,&DAT_005bf62c);
  local_14 = FUN__text__0056ce80();
  FUN__text__0056d810(local_114,param_2);
  FUN__text__004077c0(DAT_007a49fc);
  uVar7 = 2;
  puVar6 = local_114;
  uVar5 = local_14;
  uVar2 = FUN__text__004142b0(local_14,puVar6,2);
  FUN__text__00408e30(uVar2,uVar5,puVar6,uVar7);
  FUN__text__004d1bf0(&local_14);
  *(short *)(local_8 + 0x16) = *(short *)(local_8 + 0x16) + 1;
  if (9 < *(ushort *)(local_8 + 0x16)) {
    *(undefined2 *)(local_8 + 0x16) = 9;
  }
  local_8 = 0x4cadcd;
  FUN__text__0056ce80();
  return;
}

