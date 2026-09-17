
/* WARNING: Removing unreachable block (ram,0x004673b5) */
/* WARNING: Removing unreachable block (ram,0x004673d8) */
/* WARNING: Removing unreachable block (ram,0x004673e2) */

void FUN__text__00467380(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined *puVar6;
  undefined4 uVar7;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  FUN__text__004674c0();
  local_10 = 0x200;
  local_c = 0;
  do {
    if (local_c == local_10) {
LAB__text__004674a4:
      local_8 = 0x4674b1;
      FUN__text__0056ce80();
      return;
    }
    uVar7 = 1;
    puVar6 = (&PTR_DAT_006162ac)[local_c];
    uVar5 = *(undefined4 *)(local_8 + 0xdb80c);
    uVar2 = FUN__text__004142b0(uVar5,puVar6,1);
    local_14 = FUN__text__00408e30(uVar2,uVar5,puVar6,uVar7);
    if ((local_14 != 0) &&
       (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                    DAT_00618b38 + 0xb,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_14 != 0) {
      FUN__text__004674c0();
      goto LAB__text__004674a4;
    }
    FUN__text__004077c0(DAT_007a49fc);
    local_c = local_c + 1;
  } while( true );
}

