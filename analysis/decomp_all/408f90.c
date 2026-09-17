
void __thiscall FUN__text__00408f90(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(int *)(param_1 + 0x4c) != 0) && (*(int *)(param_1 + 0x2c) != 0)) &&
     (local_8 = param_1,
     iVar1 = FUN__text__0040e2a0(param_2,param_3,(int)*(short *)(param_1 + 0x40),
                                 (int)*(short *)(param_1 + 0x42)), iVar1 == 0)) {
    local_c = FUN__text__0040dcd0(6);
    *(undefined4 *)(local_c + 4) = 6;
    *(undefined1 *)(local_c + 8) = *(undefined1 *)(local_8 + 0x60);
    *(undefined1 *)(local_c + 9) = *(undefined1 *)(local_8 + 0x5c);
    *(uint *)(local_c + 0x1c) =
         (uint)*(byte *)(local_8 + 0x67) << 0x18 | (uint)*(byte *)(local_8 + 0x66) << 0x10 |
         (uint)*(byte *)(local_8 + 0x65) << 8 | (uint)*(byte *)(local_8 + 100);
    *(undefined2 *)(local_c + 10) = (undefined2)param_2;
    *(undefined2 *)(local_c + 0xc) = (undefined2)param_3;
    *(undefined2 *)(local_c + 0xe) = *(undefined2 *)(local_8 + 0x40);
    *(undefined2 *)(local_c + 0x10) = *(undefined2 *)(local_8 + 0x42);
    *(undefined2 *)(local_c + 0x12) = *(undefined2 *)(local_8 + 0x3c);
    *(undefined2 *)(local_c + 0x14) = *(undefined2 *)(local_8 + 0x3e);
    *(undefined2 *)(local_c + 0x16) = *(undefined2 *)(local_8 + 0x38);
    *(int *)(local_c + 0x20) = local_8;
    *(undefined2 *)(local_c + 0x18) = *(undefined2 *)(local_8 + 0x76);
    FUN__text__0040df20(local_c,*(undefined2 *)(local_8 + 0x76));
  }
  local_8 = 0x40912c;
  FUN__text__0056ce80();
  return;
}

