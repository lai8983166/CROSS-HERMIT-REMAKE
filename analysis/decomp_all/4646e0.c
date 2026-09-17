
void FUN__text__004646e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058fc18;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00464780();
  local_8 = 0;
  FUN__text__00464780();
  local_8 = CONCAT31(local_8._1_3_,1);
  FUN__text__004648d0(local_14);
  FUN__text__004648d0(local_14 + 0x12e8);
  ExceptionList = local_10;
  local_8 = 0x464772;
  FUN__text__0056ce80();
  return;
}

