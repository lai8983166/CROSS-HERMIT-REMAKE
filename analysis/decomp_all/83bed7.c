
/* WARNING: Instruction at (ram,0x0083beeb) overlaps instruction at (ram,0x0083beea)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x0083bf3b) */
/* WARNING: Removing unreachable block (ram,0x0083c1db) */
/* WARNING: Removing unreachable block (ram,0x0083c289) */
/* WARNING: Removing unreachable block (ram,0x0083c483) */
/* WARNING: Removing unreachable block (ram,0x0083c658) */
/* WARNING: Removing unreachable block (ram,0x0083c4e6) */
/* WARNING: Removing unreachable block (ram,0x0083c473) */
/* WARNING: Removing unreachable block (ram,0x0083c3b8) */
/* WARNING: Removing unreachable block (ram,0x0083c3d5) */
/* WARNING: Removing unreachable block (ram,0x0083c2e0) */
/* WARNING: Removing unreachable block (ram,0x0083c21a) */
/* WARNING: Removing unreachable block (ram,0x0083c179) */
/* WARNING: Removing unreachable block (ram,0x0083c196) */
/* WARNING: Removing unreachable block (ram,0x0083c0c5) */
/* WARNING: Removing unreachable block (ram,0x0083c0b5) */
/* WARNING: Removing unreachable block (ram,0x0083bf06) */
/* WARNING: Removing unreachable block (ram,0x0083bf2b) */
/* WARNING: Removing unreachable block (ram,0x0083bf87) */
/* WARNING: Removing unreachable block (ram,0x0083bfbc) */
/* WARNING: Removing unreachable block (ram,0x0083bfbe) */
/* WARNING: Removing unreachable block (ram,0x0083c055) */
/* WARNING: Removing unreachable block (ram,0x0083c0d2) */
/* WARNING: Removing unreachable block (ram,0x0083c08c) */
/* WARNING: Removing unreachable block (ram,0x0083c195) */
/* WARNING: Removing unreachable block (ram,0x0083c1cd) */
/* WARNING: Removing unreachable block (ram,0x0083c325) */
/* WARNING: Removing unreachable block (ram,0x0083c27b) */
/* WARNING: Removing unreachable block (ram,0x0083c393) */
/* WARNING: Removing unreachable block (ram,0x0083c358) */
/* WARNING: Removing unreachable block (ram,0x0083c413) */
/* WARNING: Removing unreachable block (ram,0x0083c490) */
/* WARNING: Removing unreachable block (ram,0x0083c458) */
/* WARNING: Removing unreachable block (ram,0x0083becb) */
/* WARNING: Removing unreachable block (ram,0x0083c189) */
/* WARNING: Removing unreachable block (ram,0x0083c335) */
/* WARNING: Removing unreachable block (ram,0x0083c5df) */
/* WARNING: Removing unreachable block (ram,0x0083c31a) */
/* WARNING: Removing unreachable block (ram,0x0083c1a1) */
/* WARNING: Removing unreachable block (ram,0x0083bf48) */
/* WARNING: Removing unreachable block (ram,0x0083bf47) */
/* WARNING: Removing unreachable block (ram,0x0083c267) */
/* WARNING: Removing unreachable block (ram,0x0083c33c) */
/* WARNING: Removing unreachable block (ram,0x0083c44a) */
/* WARNING: Removing unreachable block (ram,0x0083c190) */
/* WARNING: Removing unreachable block (ram,0x0083c119) */
/* WARNING: Removing unreachable block (ram,0x0083be8d) */
/* WARNING: Removing unreachable block (ram,0x0083c07e) */
/* WARNING: Removing unreachable block (ram,0x0083c554) */
/* WARNING: Removing unreachable block (ram,0x0083c48f) */
/* WARNING: Removing unreachable block (ram,0x0083c3d4) */
/* WARNING: Removing unreachable block (ram,0x0083c546) */
/* WARNING: Removing unreachable block (ram,0x0083c003) */
/* WARNING: Removing unreachable block (ram,0x0083c3c8) */
/* WARNING: Removing unreachable block (ram,0x0083bff5) */
/* WARNING: Removing unreachable block (ram,0x0083c0a0) */
/* WARNING: Removing unreachable block (ram,0x0083c4ac) */
/* WARNING: Removing unreachable block (ram,0x0083c4aa) */
/* WARNING: Removing unreachable block (ram,0x0083c0d1) */
/* WARNING: Heritage AFTER dead removal. Example location: r0x00000000 : 0x0083c34a */
/* WARNING: Heritage AFTER dead removal. Example location: s0x00000004 : 0x0083c467 */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Restarted to delay deadcode elimination for space: ram */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

undefined1 FUN__text1__0083bed7(int param_1,undefined4 param_2,uint param_3)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  bool bVar5;
  bool bVar6;
  char cVar7;
  undefined1 uVar8;
  uint uVar9;
  uint uVar10;
  int unaff_ESI;
  byte in_AF;
  byte in_TF;
  byte in_IF;
  byte in_NT;
  byte in_AC;
  byte in_ID;
  int iStackY_84;
  uint *puVar11;
  uint uStack_28;
  int iStack_c;
  int *piStack_8;
  
  bVar1 = (in_NT & 1) != 0;
  bVar2 = (in_IF & 1) != 0;
  bVar3 = (in_TF & 1) != 0;
  bVar4 = (in_AF & 1) != 0;
  bVar5 = (in_ID & 1) != 0;
  bVar6 = (in_AC & 1) != 0;
  if ((*(uint *)(DAT_00875414 + param_1 * 4) & 1) == 0) {
    cRam00000000 = cRam00000000 + (char)((uint)(&stack0xfffffffc + DAT_00875414) >> 8);
    cVar7 = FUN__text1__0083c6a2();
    if (cVar7 == '\0') {
      uVar8 = 0;
    }
    else {
      DAT_0087540c = DAT_0087540c + 1;
      FUN__text1__008487d0();
      *DAT_00875410 = param_1;
      if ((*(uint *)(iStackY_84 + 0x10) & 0xff) == 0) {
        while (DAT_0086e818 < DAT_0087540c) {
          DAT_0087540c = DAT_0087540c + -1;
          FUN__text1__0083c6a2();
          DAT_00875410[DAT_0087540c] = -1;
        }
      }
      uVar8 = 1;
    }
  }
  else if ((param_3 & 0xff) == 0) {
    if (DAT_00875420 == '\0') {
      uVar10 = param_1 * 0x1000;
      uVar9 = DAT_008753f4 + uVar10;
      uStack_28 = (uint)bVar1 * 0x4000 | (uint)SCARRY4(DAT_008753f4,uVar10) * 0x800 |
                  (uint)bVar2 * 0x200 | (uint)bVar3 * 0x100 | (uint)((int)uVar9 < 0) * 0x80 |
                  (uint)(uVar9 == 0) * 0x40 | (uint)bVar4 * 0x10 |
                  (uint)((POPCOUNT(uVar9 & 0xff) & 1U) == 0) * 4 | (uint)CARRY4(DAT_008753f4,uVar10)
                  | (uint)bVar5 * 0x200000 | (uint)bVar6 * 0x40000;
      *(undefined4 *)(unaff_ESI + -0x14) = 0;
      *(undefined4 *)(unaff_ESI + -0xc) = 0;
      VirtualProtectEx((HANDLE)*DAT_008753f0,*(LPVOID *)(unaff_ESI + -0x10),0x1000,4,
                       (PDWORD)(unaff_ESI + -0x14));
      VirtualProtectEx((HANDLE)*DAT_008753f0,*(LPVOID *)(unaff_ESI + -0x10),0x1000,
                       *(DWORD *)(unaff_ESI + -0x14),(PDWORD)(unaff_ESI + -0xc));
      uVar8 = uRam01b06133;
    }
    else {
      uVar8 = 0;
    }
  }
  else {
    uStack_28 = (uint)bVar1 * 0x4000 | (uint)bVar2 * 0x200 | (uint)bVar3 * 0x100 |
                (uint)bVar4 * 0x10 | (uint)((POPCOUNT(param_3 & 0xff) & 1U) == 0) * 4 |
                (uint)bVar5 * 0x200000 | (uint)bVar6 * 0x40000;
    puVar11 = &uStack_28;
    iStack_c = 0;
    for (piStack_8 = DAT_00875410; (iStack_c < DAT_0087540c && (*piStack_8 != param_1));
        piStack_8 = piStack_8 + 1) {
      iStack_c = iStack_c + 1;
    }
    if ((0 < iStack_c) && (iStack_c < DAT_0087540c)) {
      FUN__text1__008487d0();
      *DAT_00875410 = *(int *)((int)puVar11 + 8);
    }
    uVar8 = 1;
  }
  return uVar8;
}

