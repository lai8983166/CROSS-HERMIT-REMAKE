
void FUN__text__004d6420(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__004d6640();
  uVar1 = FUN__text__004500b0(param_1);
  uVar1 = FUN__text__0042ae20(uVar1);
  *(undefined4 *)(local_8 + 0x6414) = uVar1;
  *(undefined1 *)(local_8 + 0x6418) = 1;
  uVar1 = FUN__text__004cd700(*(undefined4 *)(local_8 + 0x6414),2);
  *(undefined4 *)(local_8 + 0x641c) = uVar1;
  uVar1 = FUN__text__004cd700(*(undefined4 *)(local_8 + 0x6414),3);
  *(undefined4 *)(local_8 + 0x6420) = uVar1;
  local_8 = 0x4d64bd;
  FUN__text__0056ce80();
  return;
}

