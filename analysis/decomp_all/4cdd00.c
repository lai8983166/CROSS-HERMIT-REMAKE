
void FUN__text__004cdd00(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puStack_c = &LAB__text__00590743;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 6;
  ExceptionList = &local_10;
  FUN__text__004d0750();
  local_8._0_1_ = 5;
  FUN__text__004c7680();
  local_8._0_1_ = 4;
  FUN__text__004c8f30();
  local_8._0_1_ = 3;
  FUN__text__004c7c80();
  local_8._0_1_ = 2;
  FUN__text__0056de40(local_14 + 0x6f60,0xe0,10,FUN__text__004c94e0);
  local_8._0_1_ = 1;
  FUN__text__0056de40(local_14 + 0x430,0xab8,10,FUN__text__004cab80);
  local_8 = (uint)local_8._1_3_ << 8;
  FUN__text__0056de40(local_14 + 0x228,0x1a,0x14,FUN__text__004cb790);
  local_8 = 0xffffffff;
  FUN__text__0056de40(local_14 + 0x1ce,0x12,5,FUN__text__004c6d40);
  ExceptionList = local_10;
  local_54[3] = 0x4cde05;
  FUN__text__0056ce80();
  return;
}

