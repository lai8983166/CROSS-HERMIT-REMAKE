
void __thiscall FUN__text__0047bc90(int param_1,int param_2,uint param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_3 & 0xff;
  local_8 = param_1;
  switch(local_c) {
  case 0:
  case 5:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e4c + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
  case 2:
  case 3:
    iVar2 = FUN__text__004690a0(param_1 + 0x80aec + *(short *)(param_2 + 0x4ee) * 0x520);
    if (iVar2 != 0) {
      *(undefined2 *)(param_2 + 0x4ee) = 0xffff;
      *(undefined2 *)(param_2 + 0x4f2) = 0xffff;
      goto LAB__text__0047be93;
    }
    *(short *)(param_2 + 0x4cc) =
         (short)((uint)*(undefined4 *)(local_8 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520) >>
                0x10);
    *(short *)(param_2 + 0x4ce) =
         (short)((uint)*(undefined4 *)(local_8 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520) >>
                0x10);
    break;
  case 4:
    *(ushort *)(param_2 + 0x4cc) = (ushort)*(byte *)(param_2 + 0x4f0) * 0x20 + 0x10;
    *(ushort *)(param_2 + 0x4ce) = (ushort)*(byte *)(param_2 + 0x4f1) * 0x10 + 8;
    break;
  case 6:
    iVar2 = FUN__text__004690a0(param_1 + 0x80aec + *(short *)(param_2 + 0x4ee) * 0x520);
    if (iVar2 != 0) {
      *(undefined2 *)(param_2 + 0x4ee) = 0xffff;
      *(undefined2 *)(param_2 + 0x4f2) = 0xffff;
      goto LAB__text__0047be93;
    }
    *(short *)(param_2 + 0x4cc) =
         (short)((uint)*(undefined4 *)(local_8 + 0x80dd8 + *(short *)(param_2 + 0x4ee) * 0x520) >>
                0x10);
    *(short *)(param_2 + 0x4ce) =
         (short)((uint)*(undefined4 *)(local_8 + 0x80ddc + *(short *)(param_2 + 0x4ee) * 0x520) >>
                0x10);
  }
  *(undefined2 *)(param_2 + 0x4d0) = *(undefined2 *)(param_2 + 0x4cc);
  *(undefined2 *)(param_2 + 0x4d2) = *(undefined2 *)(param_2 + 0x4ce);
LAB__text__0047be93:
  local_8 = 0x47bea0;
  FUN__text__0056ce80();
  return;
}

