
void __fastcall FUN__text__00415f50(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  undefined4 local_28;
  int local_24;
  undefined4 local_20;
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058ee8b;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = param_1;
  if (*(int *)(param_1 + 0xb210) != 0) {
    ExceptionList = &local_10;
    FUN__text__00416140();
    (*API_GDI32_DLL_CreateFontA)(0,0,0,0,700,0,0,0,1,5,0,0,0,&DAT_00592c9c);
    uVar1 = FUN__text__0056ce80();
    *(undefined4 *)(local_14 + 0xb26c) = uVar1;
    if (*(int *)(local_14 + 0xb26c) != 0) {
      uVar1 = FUN__text__004162c0(*(undefined4 *)(local_14 + 0xb26c));
      *(undefined4 *)(local_14 + 0xb270) = uVar1;
      if (*(int *)(local_14 + 0xb270) != 0) {
        for (local_1c = 0; local_1c != 2; local_1c = local_1c + 1) {
          local_24 = FUN__text__00428a40(0x678);
          local_8 = 0;
          if (local_24 == 0) {
            local_28 = 0;
          }
          else {
            local_28 = FUN__text__00401000((&PTR_s_FixedSys_005ff528)[local_1c],
                                           *(undefined4 *)(&DAT_005ff508 + local_1c * 4),
                                           *(undefined4 *)(&DAT_005ff520 + local_1c * 4));
          }
          local_20 = local_28;
          local_8 = 0xffffffff;
          *(undefined4 *)(local_14 + 0x1090 + local_1c * 4) = local_28;
          if (((*(int *)(local_14 + 0x1090 + local_1c * 4) == 0) ||
              (local_18 = FUN__text__004010d0(*(undefined4 *)(local_14 + 0xb210)), local_18 < 0)) ||
             (local_18 = FUN__text__00401810(), local_18 < 0)) break;
        }
      }
    }
  }
  ExceptionList = local_10;
  local_8 = 0x41612f;
  FUN__text__0056ce80();
  return;
}

