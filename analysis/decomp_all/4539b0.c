
/* WARNING: Removing unreachable block (ram,0x00453ce9) */

void __fastcall FUN__text__004539b0(int param_1)

{
  int iVar1;
  uint uVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar1 = 0x13; local_8 = param_1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  do {
    if (*(char *)(local_8 + 0x30) == '\0') {
      FUN__text__00454cf0();
      local_c = 0;
      local_c = FUN__text__00453f10();
      FUN__text__0046b470();
      FUN__text__00432100();
      FUN__text__00457aa0();
      iVar1 = FUN__text__00454c40();
      if (iVar1 == 0) {
        FUN__text__00455560();
      }
      iVar1 = FUN__text__00454c40();
      if (iVar1 == 0) {
        FUN__text__00455950();
      }
      iVar1 = FUN__text__00454c40();
      if (iVar1 == 0) {
        FUN__text__00455ec0();
      }
      iVar1 = FUN__text__00456b20();
      if (iVar1 != 0) {
        if ((*(int *)(local_8 + 0x17c) % *(int *)(local_8 + 0x180) == 0) &&
           (*(char *)(local_8 + 0x172) < '\x02')) {
          FUN__text__00416fa0(local_8 + 0x117dd8);
          local_10 = *(int *)(local_8 + 0x184);
          if (local_10 == 0) {
            FUN__text__0048ceb0();
          }
          else if (local_10 == 1) {
            iVar1 = FUN__text__00419450();
            if (iVar1 != 0) {
              iVar1 = FUN__text__00456bc0(0);
              if (iVar1 == 0) {
                FUN__text__00457030();
              }
              else {
                local_c = 1;
                *(undefined1 *)(local_8 + 0x31) = 1;
              }
              FUN__text__00415420();
            }
          }
          else if (local_10 == 3) {
            iVar1 = FUN__text__00419450();
            if (iVar1 == 0) {
              iVar1 = FUN__text__00457110(0);
              if (iVar1 != 0) {
                local_c = 1;
                *(undefined1 *)(local_8 + 0x31) = 1;
              }
              FUN__text__00415420();
            }
            else {
              FUN__text__0048d280(local_8 + 0x113bf0);
            }
            if (*(char *)(local_8 + 0x172) != '\0') {
              *(undefined1 *)(local_8 + 0x172) = 2;
            }
          }
          *(int *)(local_8 + 0x184) = *(int *)(local_8 + 0x184) + 1;
          uVar2 = *(uint *)(local_8 + 0x184) & 0x80000003;
          if ((int)uVar2 < 0) {
            uVar2 = (uVar2 - 1 | 0xfffffffc) + 1;
          }
          *(uint *)(local_8 + 0x184) = uVar2;
          *(int *)(local_8 + 0x178) = *(int *)(local_8 + 0x178) + 1;
          FUN__text__00416ff0(local_8 + 0x117dd8);
          FUN__text__00417050(local_8 + 0x117dd8);
        }
        *(int *)(local_8 + 0x17c) = *(int *)(local_8 + 0x17c) + 1;
      }
    }
    else {
      local_c = FUN__text__00453d00();
    }
    FUN__text__00453e10();
    FUN__text__0043d970();
    FUN__text__0043fd20(0xf00);
    FUN__text__0043b3c0();
    FUN__text__0046b670();
    FUN__text__00440f00(199);
    iVar1 = FUN__text__00454c40();
    if (iVar1 != 0) {
      FUN__text__00454f50();
    }
    FUN__text__00457c40();
    FUN__text__00422360(0);
  } while (local_c == 0);
  FUN__text__004967b0();
  FUN__text__00422360(0);
  FUN__text__00422360(0);
  local_8 = 0x453cf8;
  FUN__text__0056ce80();
  return;
}

