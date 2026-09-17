
void __fastcall FUN__text__00444e60(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = (undefined4 *)(param_1 + 0x1a54);
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1bb0),0,0x10);
  local_10 = 1;
  do {
    if (local_10 == 0) {
      local_8 = 0x444fef;
      FUN__text__0056ce80();
      return;
    }
    local_c = FUN__text__0044c710(&DAT_00605a70,3);
    if ((local_c != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
      local_18 = local_c;
      if (local_c == 0) {
        *(undefined4 *)(local_8 + 0x1a50) = 7;
        *local_14 = 0;
        FUN__text__004db2b0(5);
      }
      else if (local_c == 1) {
        *(undefined4 *)(local_8 + 0x1a50) = 8;
        *local_14 = 1;
        FUN__text__004db2b0(5);
      }
      else if (local_c == 2) {
        *(undefined4 *)(local_8 + 0x1a50) = 2;
        *local_14 = 0xffffffff;
        FUN__text__004db2b0(2);
      }
      else {
        iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp"
                                    ,DAT_00606718 + 0x23,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_10 = 0;
    }
    if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
      local_c = -1;
    }
    FUN__text__00445000(local_c,0xff);
    FUN__text__0044ca80();
    FUN__text__0044c9a0(0);
    FUN__text__00422360(0);
  } while( true );
}

