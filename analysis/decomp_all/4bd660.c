
void FUN__text__004bd660(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined2 local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  FUN__text__004baa90();
  if (*(short *)((int)local_8 + 0x32) == 0) {
    FUN__text__004bab60();
  }
  FUN__text__00422360(0);
  (**(code **)(*local_8 + 4))();
  FUN__text__0056ce80();
  FUN__text__00439e30(10);
  local_8 = (int *)0x4bd6e1;
  FUN__text__0056ce80();
  return;
}

