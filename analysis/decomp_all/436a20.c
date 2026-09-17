
void FUN__text__00436a20(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__004307b0();
  if (iVar1 == 0) {
    iVar1 = FUN__text__00430f60();
    if (iVar1 != 0) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
  }
  else {
    if (*(int *)(local_8 + 0x2e6f8) < 0x8ca1) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
    }
    else if (*(int *)(local_8 + 0x2e6f8) < 0xd2f1) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
    }
    else if (*(int *)(local_8 + 0x2e6f8) < 0x1a5e1) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
    }
    else {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
    }
    FUN__text__004549d0(0,0,0,1,0,0,1);
  }
  local_8 = 0x436b3a;
  FUN__text__0056ce80();
  return;
}

